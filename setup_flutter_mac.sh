#!/bin/bash
set -e

echo "============================================================"
echo "🚀 Setting up Flutter & Dart SDK for macOS (Apple Silicon)..."
echo "============================================================"

INSTALL_DIR="$HOME/development"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

if [ -d "$INSTALL_DIR/flutter" ]; then
    echo "✅ Flutter folder already exists at: $INSTALL_DIR/flutter"
else
    echo "📥 Downloading official Flutter SDK for Apple Silicon (macOS arm64)..."
    curl -o flutter.zip "https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_arm64_3.24.3-stable.zip"
    
    echo "📦 Extracting Flutter SDK..."
    unzip -q flutter.zip
    rm -f flutter.zip
    echo "✅ Flutter extracted to: $INSTALL_DIR/flutter"
fi

# Add to PATH in zshrc if not present
if ! grep -q "development/flutter/bin" "$HOME/.zshrc" 2>/dev/null; then
    echo 'export PATH="$HOME/development/flutter/bin:$PATH"' >> "$HOME/.zshrc"
    echo "✅ Added Flutter to ~/.zshrc PATH"
fi

export PATH="$HOME/development/flutter/bin:$PATH"

echo "⚙️ Pre-downloading Dart SDK & Flutter tools..."
flutter precache

echo "============================================================"
echo "🎉 Flutter & Dart Setup Complete!"
echo "📍 Flutter SDK Path: $HOME/development/flutter"
echo "📍 Dart SDK Path:    $HOME/development/flutter/bin/cache/dart-sdk"
echo "============================================================"
