#!/bin/bash
# AuraNet Dashboard Release Script

echo "🚀 AuraNet Release Manager"
echo "=========================="
echo ""

# Get current version
CURRENT_VERSION=$(cat version.txt)
echo "Current version: $CURRENT_VERSION"
echo ""

# Ask for new version
read -p "Enter new version number (e.g., 1.0.2): " NEW_VERSION

if [ -z "$NEW_VERSION" ]; then
    echo "❌ No version provided. Exiting."
    exit 1
fi

# Ask for changelog entry
echo ""
echo "Enter changelog entry (press Ctrl+D when done):"
echo "Example: Added new feature X, Fixed bug Y"
CHANGELOG_ENTRY=$(cat)

if [ -z "$CHANGELOG_ENTRY" ]; then
    echo "❌ No changelog entry provided. Exiting."
    exit 1
fi

# Update version.txt
echo "$NEW_VERSION" > version.txt
echo "✅ Updated version.txt to $NEW_VERSION"

# Update CHANGELOG.md
TODAY=$(date +%Y-%m-%d)

# Update version.json (used for OTA update checks)
python3 -c "
import json, sys
data = {'version': sys.argv[1], 'released': sys.argv[2], 'changelog': sys.argv[3]}
with open('version.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
" "$NEW_VERSION" "$TODAY" "$CHANGELOG_ENTRY"
echo "✅ Updated version.json"
sed -i "3i\\
## [$NEW_VERSION] - $TODAY\\
$CHANGELOG_ENTRY\\
" CHANGELOG.md
echo "✅ Updated CHANGELOG.md"

# Git operations
git add version.txt CHANGELOG.md version.json
git add -A  # Add any other changes
git commit -m "Release v$NEW_VERSION

$CHANGELOG_ENTRY"
echo "✅ Created git commit"

# Create git tag
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"
echo "✅ Created git tag v$NEW_VERSION"

echo ""
echo "📦 Ready to push!"
echo ""
echo "Run these commands to publish:"
echo "  git push origin main"
echo "  git push origin v$NEW_VERSION"
echo ""
echo "Or run: git push origin main --tags"
