# 🌾 GramSetu AI (ग्रामसेतु AI) - Mobile App Package

GramSetu AI is an offline, voice-first rural multi-modal assistant for Android and iOS devices.

---

### 🚀 Build & Run Commands

#### 1. Run in Debug Mode on Connected Device / Emulator:
```bash
cd mobile_app
flutter pub get
flutter run
```

#### 2. Build Standalone Release APK:
```bash
cd mobile_app
flutter build apk --release --split-per-abi
```
The generated APK will be available at:
`mobile_app/build/app/outputs/flutter-apk/app-arm64-v8a-release.apk`

---

### 📱 Key Modules Built-in:
1. **Home AI Chat & Voice Assistant:** Full on-device voice STT and TTS in Hindi with streaming bubbles.
2. **Kisan Mitra (Crop Doctor):** Disease diagnosis, chemical dosages, and Jeevamrut recipes.
3. **Yojana Sahayak:** 3-step eligibility wizard and 20+ scheme catalog.
4. **Swasthya & SOS:** Direct tap emergency call dialers (108, 102, 112) and offline first-aid triage.
5. **Rural Calculators:** Land converter (Acre to Pucca/Kaccha Bigha) and fertilizer bag calculator.
