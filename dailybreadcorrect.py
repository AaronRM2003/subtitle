import json


def replace_text_by_indexes_in_file(
    input_file,
    output_file,
    indexes,
    new_text_list
):
    # Load JSON file
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if len(indexes) != len(new_text_list):
        raise ValueError("Indexes and new_text_list length mismatch")

    for idx, new_text in zip(indexes, new_text_list):
        i = idx - 1  # convert to 0-based index

        if i < 0 or i >= len(data):
            raise IndexError(f"Index {idx} out of range")

        if "text" not in data[i]:
            raise KeyError(f"No 'text' field at index {idx}")

        # Replace ONLY the text
        data[i]["text"] = new_text

    # Write updated JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated file written to: {output_file}")

indexes_to_replace = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

new_texts =[
    {
      "en": "Holy Mary, Mother of God, we offer our wholehearted thanks for all the blessings and graces bestowed upon us and upon our nation through Kreupasanam.",
      "hi": "पवित्र मरियम, ईश्वर की माता, हम कृपासनम के माध्यम से हम पर और हमारे देश पर प्रदान की गई सभी कृपाओं और आशीर्वादों के लिए हृदय से धन्यवाद अर्पित करते हैं।",
      "ta": "கடவுளின் தாயான புனித மரியாளே, க்ருபாசனம் மூலம் எங்களுக்கும் எங்கள் தேசத்திற்கும் அளிக்கப்பட்ட அனைத்து ஆசீர்வாதங்களுக்கும் அருள்களுக்கும் எங்கள் முழு மனதுடன் நன்றி செலுத்துகிறோம்.",
      "bn": "পবিত্র মরিয়ম, ঈশ্বরের মা, ক্রেউপাসনমের মাধ্যমে আমাদের ও আমাদের দেশের ওপর দান করা সকল অনুগ্রহ ও আশীর্বাদের জন্য আমরা আন্তরিক কৃতজ্ঞতা জ্ঞাপন করি।",
      "te": "పవిత్ర మరియ, దేవుని తల్లి, క్రూపాసనమ్ ద్వారా మాకు మరియు మా దేశానికి ప్రసాదించబడిన అన్ని ఆశీర్వాదాలు మరియు కృపలకుగాను మా హృదయపూర్వక కృతజ్ఞతలను అర్పిస్తున్నాము.",
      "mr": "पवित्र मेरी, देवाची आई, क्रेउपासनमद्वारे आम्हाला व आमच्या राष्ट्राला प्रदान केलेल्या सर्व कृपा व आशीर्वादांसाठी आम्ही मनापासून कृतज्ञता अर्पण करतो.",
      "fr": "Sainte Marie, Mère de Dieu, nous rendons grâce de tout cœur pour toutes les bénédictions et grâces accordées à nous et à notre nation par l’intermédiaire de Kreupasanam.",
      "es": "Santa María, Madre de Dios, te damos gracias de todo corazón por todas las bendiciones y gracias concedidas a nosotros y a nuestra nación por medio de Kreupasanam.",
      "zh": "天主之母圣玛利亚，我们衷心感谢天主借着克鲁帕萨南赐予我们和我们国家的一切恩宠与祝福。",
      "kn": "ಪವಿತ್ರ ಮೇರಿಯೇ, ದೇವರ ತಾಯಿಯೇ, ಕ್ರೂಪಾಸನಂ ಮೂಲಕ ನಮಗೂ ನಮ್ಮ ರಾಷ್ಟ್ರಕ್ಕೂ ದಯಪಾಲಿಸಲಾದ ಎಲ್ಲಾ ಅನುಗ್ರಹಗಳು ಮತ್ತು ಆಶೀರ್ವಾದಗಳಿಗಾಗಿ ನಾವು ಹೃತ್ಪೂರ್ವಕ ಕೃತಜ್ಞತೆಯನ್ನು ಅರ್ಪಿಸುತ್ತೇವೆ."
  },
  {
      "en": "Mother, Holy Mother, Mother of God, we especially pray for the ecclesiastical approval of Your apparition at Kreupasanam on December 7, 2004, at 02:30 in the afternoon.",
      "hi": "माता, पवित्र माता, ईश्वर की माता, हम विशेष रूप से 7 दिसंबर 2004 को दोपहर 02:30 बजे कृपासनम में आपके दर्शन के संबंध में कलीसियाई स्वीकृति के लिए प्रार्थना करते हैं।",
      "ta": "அன்னையே, பரிசுத்த அன்னையே, இறைவனின் அன்னையே, 2004 டிசம்பர் 7 அன்று பிற்பகல் 02:30 மணிக்கு க்ருபாசனத்தில் நிகழ்ந்த உமது தரிசனத்திற்கான திருச்சபை அங்கீகாரத்திற்காக நாங்கள் விசேஷமாக ஜெபிக்கிறோம்.",
      "bn": "মা, পবিত্র মা, ঈশ্বরের মা, ২০০৪ সালের ৭ই ডিসেম্বর দুপুর ২:৩০ মিনিটে ক্রেউপাসনমে সংঘটিত আপনার আবির্ভাবের বিষয়ে গির্জার আনুষ্ঠানিক অনুমোদনের জন্য আমরা বিশেষভাবে প্রার্থনা করি।",
      "te": "తల్లి, పవిత్ర తల్లి, దేవుని తల్లి, 2004 డిసెంబర్ 7న మధ్యాహ్నం 02:30 గంటలకు క్రూపాసనంలో జరిగిన మీ దర్శనానికి సంబంధించి చర్చీ ఆమోదం కోసం మేము ప్రత్యేకంగా ప్రార్థిస్తున్నాము.",
      "mr": "आई, पवित्र आई, देवाची आई, 7 डिसेंबर 2004 रोजी दुपारी 02:30 वाजता क्रेउपासनम येथे झालेल्या तुमच्या प्रकटीकरणासंबंधी चर्चीय मान्यतेसाठी आम्ही विशेष प्रार्थना करतो.",
      "fr": "Mère, Sainte Mère, Mère de Dieu, nous prions tout particulièrement pour l’approbation ecclésiastique de l’apparition survenue à Kreupasanam le 7 décembre 2004 à 14h30.",
      "es": "Madre, Santa Madre, Madre de Dios, oramos especialmente por la aprobación eclesiástica de la aparición ocurrida en Kreupasanam el 7 de diciembre de 2004 a las 14:30.",
      "zh": "圣母，圣母，天主之母，我们特别为教会对您于2004年12月7日下午2:30在克鲁帕萨南显现一事的教会审慎认可而祈祷。",
      "kn": "ತಾಯಿ, ಪವಿತ್ರ ತಾಯಿ, ದೇವರ ತಾಯಿ, 2004 ಡಿಸೆಂಬರ್ 7 ರಂದು ಮಧ್ಯಾಹ್ನ 02:30 ಕ್ಕೆ ಕ್ರೂಪಾಸನಂನಲ್ಲಿ ಸಂಭವಿಸಿದ ನಿಮ್ಮ ದರ್ಶನಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ಚರ್ಚಿನ ಅನುಮೋದನೆಗಾಗಿ ನಾವು ವಿಶೇಷವಾಗಿ ಪ್ರಾರ್ಥಿಸುತ್ತೇವೆ."
  },
  {
      "en": "We pray as the Holy Church begins its ecclesiastical study of the documents submitted regarding the apparition.",
      "hi": "हम प्रार्थना करते हैं कि पवित्र कलीसिया, दर्शन से संबंधित प्रस्तुत किए गए दस्तावेज़ों के कलीसियाई अध्ययन की शुरुआत करे।",
      "ta": "இந்த தரிசனத்தைப் பற்றிய சமர்ப்பிக்கப்பட்ட ஆவணங்களை திருச்சபை ஆய்வு செய்யத் தொடங்கும் வேளையில் நாங்கள் ஜெபிக்கிறோம்.",
      "bn": "এই আবির্ভাব সংক্রান্ত দাখিলকৃত নথিপত্রের গির্জাগত অধ্যয়ন শুরু করার সময় আমরা প্রার্থনা করি।",
      "te": "దర్శనానికి సంబంధించిన సమర్పించిన పత్రాలపై చర్చి తన పరిశీలనను ప్రారంభిస్తున్నప్పుడు మేము ప్రార్థిస్తున్నాము.",
      "mr": "प्रकटीकरणासंदर्भात सादर केलेल्या कागदपत्रांचा चर्चीय अभ्यास सुरू होत असताना आम्ही प्रार्थना करतो.",
      "fr": "Nous prions tandis que la Sainte Église commence l’étude ecclésiastique des documents soumis concernant l’apparition.",
      "es": "Oramos mientras la Santa Iglesia inicia el estudio eclesiástico de los documentos presentados sobre la aparición.",
      "zh": "当圣教会开始对有关显现所提交的文件进行教会研究时，我们虔诚祈祷。",
      "kn": "ದರ್ಶನಕ್ಕೆ ಸಂಬಂಧಿಸಿದಂತೆ ಸಲ್ಲಿಸಲಾದ ದಾಖಲೆಗಳ ಚರ್ಚಿನ ಅಧ್ಯಯನವನ್ನು ಪವಿತ್ರ ಚರ್ಚ್ ಆರಂಭಿಸುತ್ತಿರುವಾಗ ನಾವು ಪ್ರಾರ್ಥಿಸುತ್ತೇವೆ."
  },
  {
      "en": "O Holy Mother, grant that this apparition may lead to the consecration of all creation to You, the Queen of Heaven and Earth, by the Holy Catholic Church, for the protection and sustenance of the world.",
      "hi": "हे पवित्र माता, यह दर्शन पवित्र कैथोलिक कलीसिया द्वारा, संसार की रक्षा और पोषण के लिए, स्वर्ग और पृथ्वी की रानी, आपको सम्पूर्ण सृष्टि के समर्पण का कारण बने।",
      "ta": "ஓ பரிசுத்த தாயே, இந்தத் தரிசனம், உலகத்தின் பாதுகாப்பிற்கும் பேணுதலுக்கும், பரிசுத்த கத்தோலிக்க திருச்சபையால், வானமும் பூமியும் ஆளும் ராணியான உமக்கு, முழு படைப்பையும் அர்ப்பணிக்க வழிவகுக்கட்டும்.",
      "bn": "হে পবিত্র মা, এই আবির্ভাব যেন পবিত্র ক্যাথলিক চার্চের মাধ্যমে, পৃথিবীর সুরক্ষা ও সংরক্ষণের জন্য, স্বর্গ ও পৃথিবীর রাণী হিসেবে তোমার কাছে সমগ্র সৃষ্টির উৎসর্গের পথে পরিচালিত করে।",
      "te": "ఓ పవిత్ర తల్లి, ఈ దర్శనం ప్రపంచ రక్షణ మరియు సంరక్షణ కొరకు, పవిత్ర కాథలిక్ చర్చీ ద్వారా, స్వర్గం మరియు భూమి యొక్క రాణి అయిన నీకు సమస్త సృష్టి అంకితమయ్యేలా దారి చూపించుగాక.",
      "mr": "हे पवित्र माते, हे प्रकटीकरण पवित्र कॅथोलिक चर्चद्वारे, जगाच्या संरक्षणासाठी व पोषणासाठी, स्वर्ग आणि पृथ्वीच्या राणी असलेल्या तुझ्याकडे सर्व सृष्टीच्या अर्पणास कारणीभूत ठरो.",
      "fr": "Ô Sainte Mère, que cette apparition conduise, par la Sainte Église catholique, à la consécration de toute la création à Vous, Reine du Ciel et de la Terre, pour la protection et le soutien du monde.",
      "es": "Oh Santa Madre, concede que esta aparición conduzca, por medio de la Santa Iglesia Católica, a la consagración de toda la creación a Ti, Reina del Cielo y de la Tierra, para la protección y el sustento del mundo.",
      "zh": "噢，圣母，愿这次显现能通过天主教圣教会，引导整个受造界奉献于您——天地之后，为世界的守护与扶持。",
      "kn": "ಓ ಪವಿತ್ರ ತಾಯಿಯೇ, ಈ ದರ್ಶನವು ಪವಿತ್ರ ಕ್ಯಾಥೋಲಿಕ್ ಚರ್ಚ್ ಮೂಲಕ, ಪ್ರಪಂಚದ ರಕ್ಷಣೆ ಮತ್ತು ಪೋಷಣೆಗೆಂದು, ಸ್ವರ್ಗ ಮತ್ತು ಭೂಮಿಯ ರಾಣಿಯಾದ ನಿನಗೆ ಸಮಸ್ತ ಸೃಷ್ಟಿಯ ಅರ್ಪಣೆಗೆ ದಾರಿ ಮಾಡಿಕೊಡಲಿ."
  },
  {
      "en": "Holy Mary, Our Lady of the Rosary, uniting all the prayers of Kreupasanam,",
      "hi": "पवित्र मरियम, रोज़री की माता, कृपासनम की सभी प्रार्थनाओं को एकत्र करते हुए,",
      "ta": "புனித மரியாளே, ஜெபமாலையின் அன்னையே, க்ருபாசனத்தின் அனைத்து ஜெபங்களையும் ஒன்றிணைத்து,",
      "bn": "পবিত্র মরিয়ম, জপমালার জননী, ক্রেউপাসনমের সকল প্রার্থনাকে একত্রিত করে,",
      "te": "పవిత్ర మరియ, రోసరీ మాత, క్రూపాసనమ్ యొక్క అన్ని ప్రార్థనలను ఏకముచేస్తూ,",
      "mr": "पवित्र मेरी, जपमाळेची माता, क्रेउपासनमच्या सर्व प्रार्थना एकत्र करत,",
      "fr": "Sainte Marie, Notre-Dame du Rosaire, rassemblant toutes les prières de Kreupasanam,",
      "es": "Santa María, Nuestra Señora del Rosario, reuniendo todas las oraciones de Kreupasanam,",
      "zh": "圣母玛利亚，玫瑰圣母，汇集克鲁帕萨南的一切祈祷，",
      "kn": "ಪವಿತ್ರ ಮೇರಿ, ಜಪಮಾಲೆಯ ಮಾತೆ, ಕ್ರೂಪಾಸನಂನ ಎಲ್ಲಾ ಪ್ರಾರ್ಥನೆಗಳನ್ನು ಒಂದುಗೂಡಿಸುತ್ತಾ,"
  },
  {
      "en": "we now place before You this special intention (state the intention here).",
      "hi": "अब हम यह विशेष मनोकामना आपके चरणों में अर्पित करते हैं (यहाँ मनोकामना व्यक्त करें)।",
      "ta": "இப்போது இந்த சிறப்பு நோக்கத்தை உமது திருப்பாதங்களில் சமர்ப்பிக்கிறோம் (நோக்கத்தை இங்கே கூறுங்கள்).",
      "bn": "আমরা এখন এই বিশেষ অভিপ্রায়টি আপনার চরণে সমর্পণ করছি (এখানে অভিপ্রায়টি বলুন)।",
      "te": "ఇప్పుడు ఈ ప్రత్యేక ఉద్దేశ్యాన్ని మీ పాదాల వద్ద సమర్పిస్తున్నాము (ఉద్దేశ్యాన్ని ఇక్కడ పేర్కొనండి).",
      "mr": "आता हा विशेष हेतू आम्ही तुमच्या चरणी अर्पण करतो (येथे हेतू सांगा).",
      "fr": "nous déposons maintenant cette intention particulière à vos pieds (indiquez l’intention ici).",
      "es": "ponemos ahora esta intención especial a tus pies (indica aquí la intención).",
      "zh": "我们现在将这特别的意向呈献在您足前（请在此说明意向）。",
      "kn": "ನಾವು ಈಗ ಈ ವಿಶೇಷ ಉದ್ದೇಶವನ್ನು ನಿಮ್ಮ ಪಾದಗಳ ಬಳಿಯಲ್ಲಿ ಅರ್ಪಿಸುತ್ತೇವೆ (ಇಲ್ಲಿ ಉದ್ದೇಶವನ್ನು ತಿಳಿಸಿ)."
  },
  {
      "en": "and have mercy on us to grant this in the blessed moment of your apparition, Amen.",
      "hi": "और कृपा कर हमारे ऊपर दया करें कि आपके दर्शन के इस धन्य क्षण में यह प्रदान हो, आमीन।",
      "ta": "உமது தரிசனத்தின் இந்த ஆசீர்வதிக்கப்பட்ட தருணத்தில் எங்கள்மேல் இரக்கம் கொண்டு இதை அருளும், ஆமென்.",
      "bn": "এবং আপনার আবির্ভাবের এই ধন্য মুহূর্তে আমাদের প্রতি করুণা করে এটি প্রদান করুন, আমিন।",
      "te": "మీ దర్శనపు ఈ ఆశీర్వాద ఘడియలో మాపై కరుణ చూపి దీనిని ప్రసాదించండి, ఆమేన్",
      "mr": "आणि तुमच्या प्रकटीकरणाच्या या धन्य क्षणी आमच्यावर दया करून हे प्रदान कर, आमेन.",
      "fr": "et, dans votre miséricorde, accordez-nous cela au moment béni de votre apparition. Amen.",
      "es": "y, en tu misericordia, concédenos esto en el momento bendito de tu aparición. Amén.",
      "zh": "并求您在显现的这神圣时刻，以慈悲垂允我们的祈求，阿们。",
      "kn": "ಮತ್ತು ನಿನ್ನ ದರ್ಶನದ ಈ ಆಶೀರ್ವಾದದ ಕ್ಷಣದಲ್ಲಿ ಕರುಣೆಯಿಂದ ಇದನ್ನು ನಮಗೆ ದಯಪಾಲಿಸು, ಆಮೆನ್."
  },
   {
    "en": "I believe in God, the Father almighty, Creator of heaven and earth, and in Jesus Christ, His only Son, our Lord,",
    "hi": "मैं सर्वशक्तिमान पिता ईश्वर में विश्वास करता हूँ, जो स्वर्ग और पृथ्वी के सृष्टिकर्ता हैं, और उनके एकमात्र पुत्र, हमारे प्रभु यीशु मसीह में।",
    "ta": "நான் சர்வவல்லமையுள்ள பிதாவாகிய கடவுளையும், வானத்தையும் பூமியையும் படைத்தவரையும், அவருடைய ஒரே குமாரனும் நம்முடைய ஆண்டவருமாகிய இயேசு கிறிஸ்துவையும் நம்புகிறேன்.",
    "bn": "আমি সর্বশক্তিমান পিতা ঈশ্বরে বিশ্বাস করি, যিনি স্বর্গ ও পৃথিবীর স্রষ্টা, এবং তাঁর একমাত্র পুত্র, আমাদের প্রভু যীশু খ্রীষ্টে।",
    "te": "నేను సర్వశక్తిమంతుడైన తండ్రి దేవుని నమ్ముతున్నాను, ఆయన స్వర్గమును భూమిని సృష్టించినవాడు, మరియు ఆయన ఏకైక కుమారుడైన మన ప్రభువు యేసు క్రీస్తును నమ్ముతున్నాను.",
    "mr": "मी सर्वशक्तिमान पिता देवावर विश्वास ठेवतो, जो स्वर्ग आणि पृथ्वीचा निर्माणकर्ता आहे, आणि त्याचा एकुलता एक पुत्र, आपला प्रभु येशू ख्रिस्त याच्यावर.",
    "fr": "Je crois en Dieu, le Père tout-puissant, créateur du ciel et de la terre, et en Jésus-Christ, son Fils unique, notre Seigneur,",
    "es": "Creo en Dios, Padre todopoderoso, Creador del cielo y de la tierra, y en Jesucristo, su único Hijo, nuestro Señor,",
    "zh": "我信天主，全能的圣父，天地的创造者；我信我主耶稣基督，天主的独生子。",
    "kn": "ನಾನು ಸರ್ವಶಕ್ತನಾದ ತಂದೆ ದೇವರಲ್ಲಿ ನಂಬಿಕೆ ಇಡುತ್ತೇನೆ, ಆತನು ಆಕಾಶಭೂಮಿಗಳ ಸೃಷ್ಟಿಕರ್ತನು, ಮತ್ತು ಆತನ ಏಕೈಕ ಪುತ್ರನಾದ ನಮ್ಮ ಕರ್ತನಾದ ಯೇಸು ಕ್ರಿಸ್ತನಲ್ಲಿ ನಂಬಿಕೆ ಇಡುತ್ತೇನೆ."
  },
  {
    "en": "who was conceived by the Holy Spirit, born of the Virgin Mary, suffered under Pontius Pilate, was crucified, died, and was buried; He descended into hell; on the third day He rose again from the dead;",
    "hi": "जो पवित्र आत्मा से गर्भ में आया, कुँवारी मरियम से जन्मा, पोंतियुस पिलातुस के अधीन दुःख सहा, क्रूस पर चढ़ाया गया, मरा और दफ़नाया गया; वह अधोलोक में उतरा; तीसरे दिन मृतकों में से जी उठा;",
    "ta": "பரிசுத்த ஆவியினால் கருத்தரிக்கப்பட்டு, கன்னி மரியாளிடமிருந்து பிறந்து, பொந்தியு பிலாத்துவின் கீழ் துன்புற்று, சிலுவையில் அறையப்பட்டு, மரித்து, அடக்கம் செய்யப்பட்டார்; அவர் பாதாளத்தில் இறங்கினார்; மூன்றாம் நாளில் அவர் இறந்தோரிலிருந்து உயிர்த்தெழுந்தார்;",
    "bn": "তিনি পবিত্র আত্মার দ্বারা গর্ভধারিত হয়ে কুমারী মরিয়মের গর্ভে জন্মগ্রহণ করেন; পন্তীয় পীলাতের অধীনে কষ্টভোগ করেন, ক্রুশবিদ্ধ হন, মৃত্যুবরণ করে সমাধিস্থ হন; তিনি পাতালে অবতরণ করেন; তৃতীয় দিনে মৃতদের মধ্য থেকে পুনরুত্থিত হন;",
    "te": "ఆయన పరిశుద్ధాత్మ ద్వారా గర్భధరింపబడి, కన్య మరియకు జన్మించాడు; పొంతియుస్ పిలాతు కాలంలో బాధపడ్డాడు; సిలువ వేయబడి, మరణించి, సమాధి చేయబడ్డాడు; ఆయన పాతాళానికి దిగిపోయాడు; మూడవ రోజున మృతులలో నుండి తిరిగి లేచాడు;",
    "mr": "तो पवित्र आत्म्यापासून गर्भधारण झाला, कुमारी मरीयेपासून जन्मला; पोंतियुस पिलाताच्या काळात दुःख सहन केले; वधस्तंभावर खिळला गेला, मरण पावला आणि पुरण्यात आला; तो अधोलोकात उतरला; तिसऱ्या दिवशी मृतांतून पुन्हा उठला;",
    "fr": "Il a été conçu du Saint-Esprit, est né de la Vierge Marie, a souffert sous Ponce Pilate, a été crucifié, est mort et a été enseveli ; il est descendu aux enfers ; le troisième jour, il est ressuscité des morts ;",
    "es": "que fue concebido por obra y gracia del Espíritu Santo, nació de Santa María Virgen, padeció bajo el poder de Poncio Pilato, fue crucificado, muerto y sepultado; descendió a los infiernos; al tercer día resucitó de entre los muertos;",
    "zh": "他因圣神降孕，由童贞玛利亚所生；在本丢·比拉多执政时受难，被钉在十字架上，死而安葬；他下降阴府；第三天从死者中复活；",
    "kn": "ಆತನು ಪವಿತ್ರಾತ್ಮನಿಂದ ಗರ್ಭಧರಿಸಲ್ಪಟ್ಟು, ಕನ್ಯೆ ಮರಿಯರಿಂದ ಜನಿಸಿದನು; ಪೊಂಟಿಯಸ್ ಪಿಲಾತನ ಆಡಳಿತದಲ್ಲಿ ದುಃಖ ಅನುಭವಿಸಿ, ಶಿಲುಬೆಗೆ ಹಾಕಲ್ಪಟ್ಟು, ಮರಣಹೊಂದಿ ಸಮಾಧಿಗೊಳಿಸಲ್ಪಟ್ಟನು; ಆತನು ಪಾತಾಳಕ್ಕೆ ಇಳಿದನು; ಮೂರನೇ ದಿನ ಸತ್ತವರೊಳಗಿಂದ ಪುನರುತ್ಥಾನಗೊಂಡನು;"
  },
  {
    "en": "He ascended into heaven and is seated at the right hand of God the Father almighty; from there He will come to judge the living and the dead.",
    "hi": "वह स्वर्ग पर चढ़ गया और सर्वशक्तिमान पिता ईश्वर के दाहिने बैठा है; वहीं से वह जीवितों और मृतकों का न्याय करने आएगा।",
    "ta": "அவர் பரலோகத்திற்கு ஏறி, சர்வவல்லமையுள்ள பிதாவாகிய கடவுளின் வலப்பக்கத்தில் வீற்றிருக்கிறார்; அங்கிருந்து அவர் உயிருள்ளவர்களையும் இறந்தவர்களையும் நீதித்தீர்ப்பு வழங்க வருவார்.",
    "bn": "তিনি স্বর্গে আরোহণ করেছেন এবং সর্বশক্তিমান পিতা ঈশ্বরের ডান পাশে অধিষ্ঠিত আছেন; সেখান থেকে তিনি জীবিত ও মৃতদের বিচার করতে আসবেন।",
    "te": "ఆయన పరలోకానికి ఆరోహణమై, సర్వశక్తిమంతుడైన తండ్రి దేవుని కుడివైపున కూర్చున్నాడు; అక్కడి నుండి ఆయన జీవులనూ మృతులనూ తీర్పు తీర్చుటకు వస్తాడు.",
    "mr": "तो स्वर्गात आरोहण झाला आणि सर्वशक्तिमान देव पित्याच्या उजव्या बाजूस बसला आहे; तेथून तो जिवंतांचा आणि मृतांचा न्याय करायला येईल.",
    "fr": "Il est monté au ciel, il est assis à la droite de Dieu le Père tout-puissant ; d’où il viendra juger les vivants et les morts.",
    "es": "Subió a los cielos y está sentado a la derecha de Dios Padre todopoderoso; desde allí ha de venir a juzgar a vivos y muertos.",
    "zh": "他升了天，坐在全能圣父的右边；他要从那里来审判生者死者。",
    "kn": "ಆತನು ಪರಲೋಕಕ್ಕೆ ಏರಿ, ಸರ್ವಶಕ್ತನಾದ ತಂದೆ ದೇವರ ಬಲಗಡೆಯಲ್ಲಿ ಆಸೀನನಾಗಿದ್ದಾನೆ; ಅಲ್ಲಿಂದ ಆತನು ಜೀವಂತರನ್ನೂ ಸತ್ತವರನ್ನೂ ನ್ಯಾಯತೀರಿಸಲು ಬರಲಿದ್ದಾನೆ."
  },
  {
    "en": "I believe in the Holy Spirit, the holy Catholic Church, the communion of saints, the forgiveness of sins,",
    "hi": "मैं पवित्र आत्मा, पवित्र कैथोलिक कलीसिया, संतों की सहभागिता और पापों की क्षमा में विश्वास करता हूँ,",
    "ta": "நான் பரிசுத்த ஆவியையும், பரிசுத்த கத்தோலிக்க திருச்சபையையும், புனிதர்களின் ஒன்றிப்பையும், பாவமன்னிப்பையும் நம்புகிறேன்.",
    "bn": "আমি পবিত্র আত্মায়, পবিত্র ক্যাথলিক গির্জায়, সাধুদের মিলনে এবং পাপের ক্ষমায় বিশ্বাস করি,",
    "te": "నేను పరిశుద్ధాత్మను, పవిత్ర కాథలిక్ సంఘాన్ని, సాధువుల సంఘమును మరియు పాప క్షమాపణను నమ్ముతున్నాను,",
    "mr": "मी पवित्र आत्म्यावर, पवित्र कॅथोलिक चर्चवर, संतांच्या सहभागावर आणि पापांच्या क्षमेवर विश्वास ठेवतो,",
    "fr": "Je crois en l’Esprit Saint, à la sainte Église catholique, à la communion des saints, au pardon des péchés,",
    "es": "Creo en el Espíritu Santo, la santa Iglesia católica, la comunión de los santos, el perdón de los pecados,",
    "zh": "我信圣神；我信至圣公教会；我信诸圣相通；我信罪得赦免，",
    "kn": "ನಾನು ಪವಿತ್ರಾತ್ಮನಲ್ಲಿ, ಪವಿತ್ರ ಕ್ಯಾಥೋಲಿಕ್ ಸಭೆಯಲ್ಲಿ, ಸಂತರ ಸಹಭಾಗಿತ್ವದಲ್ಲಿ ಮತ್ತು ಪಾಪಗಳ ಕ್ಷಮೆಯಲ್ಲಿ ನಂಬಿಕೆ ಇಡುತ್ತೇನೆ."
  },
  {
    "en": "the resurrection of the body, and life everlasting. Amen.",
    "hi": "शरीर के पुनरुत्थान और अनन्त जीवन में। आमीन।",
    "ta": "உடலின் உயிர்த்தெழுதலையும் நித்திய ஜீவனையும் நம்புகிறேன். ஆமென்.",
    "bn": "দেহের পুনরুত্থান এবং অনন্ত জীবনে বিশ্বাস করি। আমেন।",
    "te": "శరీర పునరుత్థానమును మరియు నిత్యజీవమును నమ్ముతున్నాను. ఆమేన్.",
    "mr": "शरीराचे पुनरुत्थान आणि अनंत जीवनावर विश्वास ठेवतो. आमेन.",
    "fr": "à la résurrection de la chair et à la vie éternelle. Amen.",
    "es": "la resurrección de la carne y la vida eterna. Amén.",
    "zh": "我信肉身复活；我信永生。阿们。",
    "kn": "ದೇಹದ ಪುನರುತ್ಥಾನವನ್ನು ಮತ್ತು ನಿತ್ಯಜೀವನವನ್ನು ನಂಬುತ್ತೇನೆ. ಆಮೆನ್."
  },


   {
  "en": "Our Father, who art in heaven, hallowed be Thy name. Thy kingdom come, Thy will be done, on earth as it is in heaven.",
  "hi": "हे हमारे पिता, जो स्वर्ग में हैं, तेरा नाम पवित्र माना जाए। तेरा राज्य आए। तेरी इच्छा जैसे स्वर्ग में पूरी होती है, वैसे पृथ्वी पर भी हो।",
  "ta": "விண்ணகத்தில் இருக்கிற எங்கள் தந்தையே, உமது நாமம் புனிதப்படுத்தப்படுக. உமது ராஜ்யம் வருக; விண்ணகத்தில் போல பூமியிலும் உமது சித்தம் நிறைவேறுக.",
  "bn": "হে আমাদের স্বর্গস্থ পিতা, তোমার নাম পবিত্র মানা হোক। তোমার রাজ্য আসুক। তোমার ইচ্ছা যেমন স্বর্গে পূর্ণ হয়, তেমনই পৃথিবীতেও হোক।",
  "te": "పరలోకమందున్న మా తండ్రి, నీ నామము పరిశుద్ధపరచబడుగాక. నీ రాజ్యము రాగాక; నీ చిత్తము పరలోకమందు జరిగునట్లు భూమిమందును జరుగుగాక.",
  "mr": "स्वर्गात असलेल्या आमच्या पित्या, तुझे नाव पवित्र मानले जावो. तुझे राज्य येवो. तुझी इच्छा जशी स्वर्गात आहे तशी पृथ्वीवरही होवो.",
  "fr": "Notre Père, qui es aux cieux, que ton nom soit sanctifié, que ton règne vienne, que ta volonté soit faite sur la terre comme au ciel.",
  "es": "Padre nuestro que estás en el cielo, santificado sea tu nombre. Venga tu reino. Hágase tu voluntad en la tierra como en el cielo.",
  "zh": "我们在天之父，愿你的名受显扬。愿你的国来临。愿你的旨意承行于世，如在天上。",
  "kn": "ಸ್ವರ್ಗದಲ್ಲಿರುವ ನಮ್ಮ ತಂದೆಯೇ, ನಿಮ್ಮ ನಾಮವು ಪವಿತ್ರವಾಗಿರಲಿ. ನಿಮ್ಮ ರಾಜ್ಯವು ಬರುವಲಿ. ನಿಮ್ಮ ಇಚ್ಛೆಯು ಸ್ವರ್ಗದಲ್ಲಿರುವಂತೆ ಭೂಮಿಯಲ್ಲಿಯೂ ನಡೆಯಲಿ."
},
{
  "en": "Give us this day our daily bread, and forgive us our trespasses, as we forgive those who trespass against us.",
  "hi": "आज हमें हमारी दैनिक रोटी दे, और हमारे अपराध क्षमा कर, जैसे हम भी अपने अपराधियों को क्षमा करते हैं।",
  "ta": "இன்றைக்கு எங்கள் அன்றாட அப்பத்தை எங்களுக்கு அளியுங்கள்; எங்களுக்கு எதிராகக் குற்றம் செய்தவர்களை நாங்கள் மன்னிப்பதுபோல், எங்கள் குற்றங்களையும் மன்னியுங்கள்.",
  "bn": "আজ আমাদের দৈনন্দিন আহার দাও, এবং আমরা যেভাবে আমাদের অপরাধীদের ক্ষমা করি, তেমনই আমাদের অপরাধ ক্ষমা করো।",
  "te": "ఈ దినమున మా దినసరి ఆహారము మాకు దయచేయుము; మేము మాపై అపరాధము చేసినవారిని క్షమించునట్లు, మా అపరాధములను మన్నించుము.",
  "mr": "आज आम्हाला आमचे दैनंदिन अन्न दे आणि आम्ही आमच्याविरुद्ध अपराध करणाऱ्यांना क्षमा करतो तसेच आमचे अपराधही क्षमा कर.",
  "fr": "Donne-nous aujourd'hui notre pain de ce jour, et pardonne-nous nos offenses, comme nous pardonnons aussi à ceux qui nous ont offensés.",
  "es": "Danos hoy nuestro pan de cada día; y perdona nuestras ofensas, como también nosotros perdonamos a los que nos ofenden.",
  "zh": "求你今天赐给我们日用的食粮，宽恕我们的罪过，如同我们宽恕得罪我们的人。",
  "kn": "ನಮ್ಮ ದಿನನಿತ್ಯದ ಅನ್ನವನ್ನು ಇಂದಿನ ದಿನಕ್ಕೆ ನಮಗೆ ದಯಪಾಲಿಸಿರಿ; ನಮ್ಮ ವಿರುದ್ಧ ತಪ್ಪು ಮಾಡಿದವರನ್ನು ನಾವು ಕ್ಷಮಿಸುವಂತೆ ನಮ್ಮ ತಪ್ಪುಗಳನ್ನೂ ಕ್ಷಮಿಸಿರಿ."
},
{
  "en": "And lead us not into temptation, but deliver us from evil. Amen.",
  "hi": "और हमें परीक्षा में न डाल, बल्कि बुराई से बचा। आमीन।",
  "ta": "எங்களைச் சோதனையில் ஆளாதிருத்து, தீமையிலிருந்து எங்களை விடுவியுங்கள். ஆமென்.",
  "bn": "আমাদের প্রলোভনে পড়তে দিও না, বরং অশুভ থেকে আমাদের রক্ষা করো। আমিন।",
  "te": "మమ్మును శోధనలోనికి నడిపింపక, చెడునుండి మమ్మును విడిపించుము. ఆమేన్.",
  "mr": "आम्हाला प्रलोभनात नेऊ नकोस, तर वाईटापासून आम्हाला वाचव. आमेन.",
  "fr": "Et ne nous laisse pas entrer en tentation, mais délivre-nous du mal. Amen.",
  "es": "No nos dejes caer en la tentación y líbranos del mal. Amén.",
  "zh": "不要让我们陷入诱惑，但救我们免于凶恶。阿门。",
  "kn": "ನಮ್ಮನ್ನು ಪ್ರಲೋಭನಕ್ಕೆ ಒಳಪಡಿಸದೆ, ದುಷ್ಟತನದಿಂದ ನಮ್ಮನ್ನು ರಕ್ಷಿಸಿರಿ. ಆಮೆನ್."
},
    {
  "en": "Hail Mary, full of grace, the Lord is with thee. Blessed art thou among women, and blessed is the fruit of thy womb, Jesus.",
  "hi": "हे मरियम, कृपा से पूर्ण, प्रभु तेरे साथ हैं। तू स्त्रियों में धन्य है, और तेरे गर्भ का फल यीशु धन्य है।",
  "ta": "அருள்மிகு மரியே, ஆண்டவர் உங்களுடன் இருக்கிறார். பெண்களிலே நீர் ஆசீர்வதிக்கப்பட்டவர்; உமது கர்ப்பத்தின் கனியாகிய இயேசு ஆசீர்வதிக்கப்பட்டவர்.",
  "bn": "হে মেরি, করুণায় পরিপূর্ণা, প্রভু তোমার সঙ্গে আছেন। তুমি নারীদের মধ্যে ধন্য, এবং তোমার গর্ভের ফল যীশু ধন্য।",
  "te": "హెయిల్ మరియం, కృపతో నిండినదానా, ప్రభువు నీతో ఉన్నాడు. నీవు స్త్రీలలో ధన్యురాలివి, నీ గర్భఫలమైన యేసు ధన్యుడు.",
  "mr": "हे मेरी, कृपेने परिपूर्ण, प्रभू तुझ्याबरोबर आहे. स्त्रियांमध्ये तू धन्य आहेस आणि तुझ्या गर्भाचे फळ येशू धन्य आहे.",
  "fr": "Je vous salue, Marie, pleine de grâce, le Seigneur est avec vous. Vous êtes bénie entre toutes les femmes, et Jésus, le fruit de vos entrailles, est béni.",
  "es": "Dios te salve, María, llena eres de gracia, el Señor es contigo. Bendita tú eres entre todas las mujeres, y bendito es el fruto de tu vientre, Jesús.",
  "zh": "万福玛利亚，你充满圣宠，主与你同在。你在妇女中受赞福，你胎中的圣子耶稣同受赞福。",
  "kn": "ಹೆಲ್ ಮರಿಯಂ, ಕೃಪೆಯಿಂದ ತುಂಬಿದವಳೆ, ಕರ್ತನು ನಿನ್ನೊಂದಿಗಿದ್ದಾನೆ. ನೀನು ಸ್ತ್ರೀಯರೊಳಗೆ ಆಶೀರ್ವಾದಿತಳು; ನಿನ್ನ ಗರ್ಭಫಲ ಯೇಸು ಆಶೀರ್ವಾದಿತನು."
},
{
  "en": "Holy Mary, Mother of God, pray for us sinners, now and at the hour of our death. Amen.",
  "hi": "हे पवित्र मरियम, ईश्वर की माता, हम पापियों के लिए अब और हमारी मृत्यु के समय प्रार्थना करें। आमीन।",
  "ta": "புனித மரியே, கடவுளின் தாயே, எங்கள் பாவிகளுக்காக இப்பொழுதும் எங்கள் மரண நேரத்திலும் பிரார்த்தனை செய்யுங்கள். ஆமென்.",
  "bn": "পবিত্র মেরি, ঈশ্বরের জননী, আমাদের পাপীদের জন্য এখন এবং আমাদের মৃত্যুর সময় প্রার্থনা করো। আমিন।",
  "te": "పవిత్ర మరియం, దేవుని తల్లి, మేము పాపులైన మా కోసం ఇప్పుడు మరియు మా మరణ సమయంలో ప్రార్థించుము. ఆమేన్.",
  "mr": "पवित्र मेरी, देवाची आई, आम्हा पाप्यांसाठी आता आणि आमच्या मृत्यूच्या वेळी प्रार्थना कर. आमेन.",
  "fr": "Sainte Marie, Mère de Dieu, priez pour nous pauvres pécheurs, maintenant et à l'heure de notre mort. Amen.",
  "es": "Santa María, Madre de Dios, ruega por nosotros pecadores, ahora y en la hora de nuestra muerte. Amén.",
  "zh": "天主圣母玛利亚，请为我们罪人现在和我们临终时祈祷。阿门。",
  "kn": "ಪವಿತ್ರ ಮರಿಯಂ, ದೇವರ ತಾಯಿ, ನಮ್ಮ ಪಾಪಿಗಳಿಗಾಗಿ ಈಗ ಮತ್ತು ನಮ್ಮ ಮರಣಕಾಲದಲ್ಲಿ ಪ್ರಾರ್ಥಿಸು. ಆಮೆನ್."
}


]


replace_text_by_indexes_in_file(
    input_file="merged_subtitles_english_time.json",
    output_file="merged_subtitles_english_time.json",
    indexes=indexes_to_replace,
    new_text_list=new_texts
)
