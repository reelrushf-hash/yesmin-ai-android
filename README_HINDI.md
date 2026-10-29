# YESMIN AI Android APK (Hindi Guide)

यह एक शुरुआती Kivy Android ऐप टेम्पलेट है। इसमें चैट बॉक्स, Send बटन और Gemini API से जवाब पाने की सुविधा है।

## जरूरी सुरक्षा बात
- अपनी Gemini API key को GitHub पर, किसी सार्वजनिक फ़ाइल में, या किसी को चैट में साझा न करें।
- इस ऐप में API key टाइप करने पर यह केवल ऐप की चलती हुई session memory में रहती है; ऐप बंद करने पर दोबारा डालनी होगी।
- यह व्यक्तिगत परीक्षण के लिए है। सार्वजनिक रूप से ऐप जारी करने से पहले API key को सुरक्षित server/backend के पीछे रखना चाहिए, क्योंकि मोबाइल ऐप से सीधे API key इस्तेमाल करना पूरी तरह सुरक्षित नहीं है।
- Gemini API की उपलब्धता, बिलिंग/कोटा और मॉडल access आपके Google AI Studio सेटअप पर निर्भर करते हैं।

## मोबाइल से APK बनाने के चरण (GitHub Actions)

1. GitHub पर लॉगिन करें और नया repository बनाएँ, जैसे `yesmin-ai-android`.
2. इस ZIP की सभी फ़ाइलें extract करें और repository में upload करें। `.github/workflows/android-apk.yml` का path ठीक यही रहना चाहिए।
3. फ़ाइलें commit करके branch का नाम `main` रखें।
4. Repository में **Actions** tab खोलें।
5. **Build YESMIN AI APK** workflow चुनें और **Run workflow** दबाएँ। पहली बार push के बाद workflow अपने-आप भी चल सकता है।
6. Workflow पूरा होने पर उसके run page के नीचे **Artifacts** में `YESMIN-AI-debug-APK` डाउनलोड करें।
7. ZIP artifact को फोन में extract करें। APK फ़ाइल खोलें। Android अगर अनुमति माँगे तो केवल अपने भरोसेमंद build के लिए उस source से app install करने की अनुमति दें।
8. ऐप खोलें, Gemini API key डालें और संदेश भेजकर टेस्ट करें।

## बिल्ड विफल हो तो
Actions → workflow run → failed step का log खोलें और आखिरी error की तस्वीर/कॉपी भेजें। API key या कोई secret log में न भेजें।

## स्थानीय Termux बिल्ड
Termux पर Android SDK/NDK और Buildozer का सेटअप कई बार कठिन/असफल हो सकता है। इसलिए इस template में GitHub Actions का Ubuntu runner इस्तेमाल किया गया है।
