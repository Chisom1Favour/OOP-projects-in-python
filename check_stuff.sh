#!/data/data/com.termux/files/usr/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Starting Auto Claim Bot Installation...${NC}"
sleep 2

# Check if running in Termux
if [ ! -d "/data/data/com.termux/files/usr" ]; then
    echo -e "${RED}❌ Error: This script must be run in Termux${NC}"
    exit 1
fi

# Update packages
echo -e "${YELLOW}📦 Updating Termux packages...${NC}"
pkg update -y && pkg upgrade -y

# Install required Termux packages
echo -e "${YELLOW}📦 Installing required Termux packages...${NC}"
pkg install -y python wget git proot-distro

# Install Alpine distro if not present
if ! proot-distro list | grep -q "alpine"; then
    echo -e "${YELLOW}📦 Installing Alpine Linux in Termux...${NC}"
    proot-distro install alpine
fi

# Set up packages in Alpine (Chromium, Chromedriver, Tesseract, Python deps)
echo -e "${YELLOW}📦 Setting up dependencies in Alpine...${NC}"
proot-distro login alpine << EOF
apk update
apk add --no-cache chromium chromium-chromedriver python3 py3-pip tesseract-ocr tesseract-ocr-data-eng py3-pillow
pip install selenium pytesseract fake-useragent
echo -e "${GREEN}✅ Installed in Alpine: Chromium \$(chromium-browser --version), Chromedriver \$(chromedriver --version)${NC}"
EOF

# Create wrapper to run Python in Alpine (binds Termux home to Alpine /root for file sharing)
echo -e "${YELLOW}📦 Creating Alpine Python wrapper (use: alpine-python your_script.py)...${NC}"
mkdir -p ~/bin
cat > ~/bin/alpine-python << 'EOW'
#!/data/data/com.termux/files/usr/bin/bash
proot-distro login alpine --isolated --fix-low-ports --bind=/data/data/com.termux/files/home:/root -- python3 "\$@"
EOW
chmod +x ~/bin/alpine-python
export PATH="$HOME/bin:$PATH"

# Create bot directory
echo -e "${YELLOW}📁 Building Auto Claim Bot project structure...${NC}"
cd ~
mkdir -p auto_claim_bot/src
mkdir -p auto_claim_bot/config
mkdir -p auto_claim_bot/scripts

# Download the main script
echo -e "${YELLOW}⬇️ Downloading bot source code...${NC}"

# Download Python source files into ~/auto_claim_bot/src/
cd auto_claim_bot/src
wget https://raw.githubusercontent.com/Chisom1Favour/Auto_claim/main/src/main.py
wget https://raw.githubusercontent.com/Chisom1Favour/Auto_claim/main/src/web_claimer.py
wget https://raw.githubusercontent.com/Chisom1Favour/Auto_claim/main/src/config_utils.py

# Download config template into ~/auto_claim_bot/config/
cd ../config
wget https://raw.githubusercontent.com/Chisom1Favour/Auto_claim/main/config/websites_template.json
cp websites_template.json websites.json

# Download run script into ~/auto_claim_bot/scripts/
cd ../scripts
wget https://raw.githubusercontent.com/Chisom1Favour/Auto_claim/main/scripts/run_bot.sh

# Make the main run script executable
chmod +x run_bot.sh

# Create the setup wizard Python script in the bot directory
echo -e "${YELLOW}📝 Creating setup wizard...${NC}"
cd ..
cat > setup_wizard.py << 'EOF'
#!/data/data/com.termux/files/usr/bin/python3
import json
import os

print("🎯 Auto Claim Bot Setup Wizard")
print("=" * 40)

config_path = "config/websites.json"

# Load existing config or create new
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
else:
    config = {}

while True:
    print(f"\nCurrent websites: {list(config.keys())}")
    print("\n1. Add new website")
    print("2. Edit existing website")
    print("3. Remove website")
    print("4. View all websites")
    print("5. Save and exit")

    choice = input("\nChoose option (1-5): ").strip()

    if choice == "1":
        name = input("Website nickname (e.g., 'amazon_rewards'): ").strip()
        url = input("Website URL: ").strip()
 username = input("Username: ").strip()
        password = input("Password: ").strip()

        config[name] = {
            "url": url,
            "username": username,
            "password": password,
            "username_id": input("Username field ID (press Enter for 'username'): ").strip() or "username",
            "password_id": input("Password field ID (press Enter for 'password'): ").strip() or "password",
            "claim_selector": input("Claim button XPath (press Enter for default): ").strip() or "//button[contains(., 'Claim')]"
        }
        print(f"✅ Added {name}")

    elif choice == "2":
        print("\n📝 Edit Website")
        site_to_edit = input("Enter the nickname of the website to edit: ").strip()
        if site_to_edit in config:
            print(f"Editing {site_to_edit}. Press Enter to keep current value.")
            current_data = config[site_to_edit]

            new_url = input(f"URL [{current_data['url']}]: ").strip()
            if new_url: current_data['url'] = new_url

            new_username = input(f"Username [{current_data['username']}]: ").strip()
            if new_username: current_data['username'] = new_username

            new_password = input(f"Password [hidden]: ").strip()
            if new_password: current_data['password'] = new_password

            new_username_id = input(f"Username field ID [{current_data['username_id']}]: ").strip()
            if new_username_id: current_data['username_id'] = new_username_id

            new_password_id = input(f"Password field ID [{current_data['password_id']}]: ").strip()
            if new_password_id: current_data['password_id'] = new_password_id

            new_claim_selector = input(f"Claim button XPath [{current_data['claim_selector']}]: ").strip()
            if new_claim_selector: current_data['claim_selector'] = new_claim_selector

            print(f"✅ Updated {site_to_edit}")
        else:
            print("❌ Website not found!")

    elif choice == "3":
        print("\n🗑️  Remove Website")
        site_to_remove = input("Enter the nickname of the website to remove: ").strip()
        if site_to_remove in config:
            del config[site_to_remove]
            print(f"✅ Removed {site_to_remove}")
        else:
            print("❌ Website not found!")

    elif choice == "4":
        print("\n📋 All Configured Websites:")
        if config:
            for name, data in config.items():
                print(f"\n{name}:")
		 print(f"  URL: {data['url']}")
                print(f"  Username: {data['username']}")
                print(f"  Username ID: {data['username_id']}")
                print(f"  Password ID: {data['password_id']}")
                print(f"  Claim Selector: {data['claim_selector']}")
                # Don't print password for security
        else:
            print("No websites configured yet.")

    elif choice == "5":
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print("✅ Configuration saved to 'config/websites.json'!")
        break

    else:
        print("❌ Invalid option. Please choose 1-5.")

print("\nSetup complete! Run 'python setup_wizard.py' to configure, then './scripts/run_bot.sh' to start (it will use Alpine for Selenium).")
EOF

# Verify installation with a quick test
echo -e "${YELLOW}🧪 Running a quick Selenium test in Alpine...${NC}"
cat > ~/test_bot.py << 'EOT'
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
driver.get("https://www.google.com")
print("Title:", driver.title)
driver.quit()
EOT
alpine-python ~/test_bot.py

echo -e "${GREEN}✅ Installation complete!${NC}"
echo -e "${BLUE}ℹ️ Run 'python ~/auto_claim_bot/setup_wizard.py' to configure websites.${NC}"
echo -e "${BLUE}ℹ️ Then run 'cd ~/auto_claim_bot/scripts && ./run_bot.sh' to start the bot.${NC}"
echo -e "${BLUE}ℹ️ In your bot code (e.g., web_claimer.py), use: webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options) with --headless, --no-sandbox, --disable-dev-shm-usage.${NC}"
echo -e "${BLUE}ℹ️ If run_bot.sh uses 'python3', update it to 'alpine-python' for Selenium compatibility.${NC}"

