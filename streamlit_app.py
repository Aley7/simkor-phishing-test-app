import streamlit as st
# import time # Artık time.sleep kullanmayacağımız için bunu yoruma alabiliriz

# --- Konfigürasyon ---
st.set_page_config(
    page_title="SimKor - Oltalama Testi",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Başlangıç ve Açıklama ---
st.title("🛡️ SimKor Oltalama (Phishing) Maili Tanıma Oyunu")
st.markdown("""
Siber güvenliğin en zayıf halkası insandır. Bu mini oyun ile oltalama (phishing) maili tanıma becerilerinizi test edin! 
Her doğru cevap için puan kazanacak, yanlış cevaplar için ise ipuçları alacaksınız.
""")

st.info("Oyunu başlatmak için aşağıdaki butona tıklayın!")

# Session State Değişkenleri
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'show_explanation' not in st.session_state: # Açıklamayı gösterip göstermeyeceğimizi tutacak
    st.session_state.show_explanation = False
if 'last_answer_correct' not in st.session_state: # Son cevabın doğru olup olmadığını tutacak
    st.session_state.last_answer_correct = False
if 'last_explanation' not in st.session_state: # Son açıklama metnini tutacak
    st.session_state.last_explanation = ""
if 'last_hint' not in st.session_state: # Son ipucu metnini tutacak
    st.session_state.last_hint = ""


questions = [
    {
        "id": 1,
        "type": "email",
        "title": "Soru 1: Hangi Mail Oltalama Olabilir?",
        "options": {
            "A": {
                "sender": "noreply@bankaniz.com.tr",
                "subject": "Acil Hesap Güncellemesi Gerekiyor",
                "body": "Değerli müşterimiz, hesabınızda şüpheli aktiviteler tespit edilmiştir. Hesabınızın askıya alınmaması için aşağıdaki bağlantıdan giriş yaparak bilgilerinizi güncelleyin: [Buraya Tıklayın](https://www.google.com/search?q=https://guvenli-bankacilik.com/update%3Fid%3D123)",
                "is_phishing": True,
                "hint": "Bu bir oltalama girişimiydi! Bankalar genellikle e-posta ile hesap güncellemesi istemez ve sizden şüpheli linklere tıklamanızı beklemez. Linkin alan adı (guvenli-bankacilik.com) sahte görünüyor ve genellikle gerçek banka adresiyle eşleşmez. Her zaman linklerin üzerine gelip gerçek hedefi kontrol edin veya doğrudan bankanın kendi web sitesine gidin.",
                "why_phishing": "Bankalar e-posta ile acil hesap güncellemesi istemez. Linkin URL'si resmi banka sitesi değil, sahte bir alan adıdır. Aciliyet hissi yaratıp panikle hareket etmenizi sağlar."
            },
            "B": {
                "sender": "destek@gercekbanka.com",
                "subject": "Hesap Özeti Bildirimi",
                "body": "Hesap özetiniz ekte sunulmuştur. Güvenliğiniz için şifreli PDF olarak gönderilmiştir. PDF şifresi: Son 4 hanesi TC kimlik numaranızın ilk 4 hanesidir.",
                "is_phishing": False,
                "hint": "Bu bir oltalama maili değil. Ancak yine de ekleri açarken ve şifre girerken her zaman dikkatli olmakta fayda var. Bilmediğiniz bir kaynaktan gelen ekleri açmayın.",
                "why_phishing": "" # Bu seçenek phishing değil, o yüzden açıklama yok.
            }
        }
    },
    {
        "id": 2,
        "type": "email",
        "title": "Soru 2: Bir Kargo Şirketinden Gelen Bu Mail Güvenli mi?",
        "options": {
            "A": {
                "sender": "info@kargom.com",
                "subject": "Kargonuz Gümrükte Bekliyor",
                "body": "Sayın Müşterimiz, 123456789 numaralı kargonuz gümrükte takılmıştır. Teslimat için 5.99 TL ek ücret ödemeniz gerekmektedir. Ödeme yapmak için acil olarak linke tıklayın: [Ödeme Yap](https://www.google.com/search?q=https://kargotakip-acil.net/odeme)",
                "is_phishing": True,
                "hint": "Bu bir oltalama girişimiydi! Kargo şirketleri genellikle ek ödemeyi bu yolla istemez ve gümrük işlemleri için farklı prosedürler izler. Linkin alan adına dikkat edin (kargotakip-acil.net); resmi kargo firmasının web sitesi değildir.",
                "why_phishing": "Kargo şirketleri gümrük ücretini e-posta ile link üzerinden ödeme istemez. Linkin alan adı sahte (gerçek kargo firmasıyla alakası yok). Aciliyet hissi ve düşük ücretle cazibe yaratır."
            },
            "B": {
                "sender": "iletisim@gercekkargo.com.tr",
                "subject": "Kargo Takip Bilgisi",
                "body": "123456789 numaralı kargonuz yola çıkmıştır. Takip numaranız: TRK123456789. Takip için web sitemizi ziyaret edebilirsiniz: [www.gercekkargo.com.tr](https://www.google.com/search?q=www.gercekkargo.com.tr)",
                "is_phishing": False,
                "hint": "Bu mail, genellikle kargo firmalarından bekleyeceğiniz standart bir takip bildirimidir. Güvenli görünüyor. Link de resmi siteye yönlendiriyor.",
                "why_phishing": ""
            }
        }
    },
    {
        "id": 3,
        "type": "message",
        "title": "Soru 3: Sosyal Medyadan Gelen Bu Mesaj Güvenli mi?",
        "options": {
            "A": {
                "sender": "Arkadaşın X",
                "subject": "Bu Komik Videoyu Görmelisin!",
                "body": "Hey, bu videoyu mutlaka izlemelisin! Çok güleceksin: [Video Linki](https://www.google.com/search?q=http://harikavideolar-com.xyz/izle)",
                "is_phishing": True,
                "hint": "Bu bir oltalama girişimiydi! Tanıdık birinden gelse bile, özellikle de alan adı (harikavideolar-com.xyz) garip görünen linklere tıklamayın. Arkadaşınızın hesabı çalınmış olabilir veya size zararlı yazılım göndermeye çalışıyor olabilirler. Linki doğrudan web tarayıcısına yazarak kontrol etmek veya arkadaşınızla başka bir yolla (telefon vb.) teyit etmek daha güvenlidir.",
                "why_phishing": "Tanıdık birinden gelse bile, şüpheli alan adlarına sahip linklere tıklanmamalıdır. Arkadaşın hesabı ele geçirilmiş olabilir. Merak uyandırıcı başlıklarla tıklamaya teşvik eder."
            },
            "B": {
                "sender": "Arkadaşın Y",
                "subject": "Nasılsın?",
                "body": "Selam, uzun zaman oldu. Nasılsın? :)",
                "is_phishing": False,
                "hint": "Bu, normal bir iletişim mesajına benziyor. Güvenli görünüyor. Ancak yine de tanımadığınız kişilerden gelen ani mesajlara veya aşırı kişisel sorulara şüpheyle yaklaşın.",
                "why_phishing": ""
            }
        }
    }
]

def next_question():
    st.session_state.question_index += 1
    st.session_state.show_explanation = False # Yeni soruya geçerken açıklamayı gizle
    st.session_state.last_answer_correct = False
    st.session_state.last_explanation = ""
    st.session_state.last_hint = ""
    st.rerun()

def display_question(q):
    st.subheader(q["title"])
    st.write("---")
    
    col1, col2 = st.columns(2)

    for idx, (option_key, option_data) in enumerate(q["options"].items()):
        
        current_col = col1 if idx % 2 == 0 else col2

        with current_col:
            st.markdown(f"**Seçenek {option_key}:**")
            if q["type"] == "email":
                st.markdown(f"**Gönderen:** `{option_data['sender']}`")
                st.markdown(f"**Konu:** `{option_data['subject']}`")
                st.markdown(f"**Mesaj:** {option_data['body']}")
            elif q["type"] == "message":
                st.markdown(f"**Gönderen:** `{option_data['sender']}`")
                st.markdown(f"**Konu:** `{option_data['subject']}`") 
                st.markdown(f"**Mesaj:** {option_data['body']}")
            
            # Açıklama gösterilmiyorsa veya bu sorunun cevabı henüz verilmediyse butonları göster
            if not st.session_state.show_explanation:
                if st.button(f"Bu Oltalama mı? (Seçenek {option_key})", key=f"q{q['id']}_opt{option_key}"):
                    process_answer(option_data['is_phishing'], q["id"], q["options"], option_data['why_phishing'])
            st.write("---")

def process_answer(is_phishing_selected, question_id, options, why_phishing_explanation):
    st.session_state.game_started = True 
    st.session_state.show_explanation = True # Açıklamayı göstermek için bayrağı ayarla

    if is_phishing_selected:
        st.session_state.score += 10
        st.session_state.last_answer_correct = True
        st.session_state.last_explanation = why_phishing_explanation
        st.balloons() 
    else:
        st.session_state.last_answer_correct = False
        # Kullanıcının hangi seçeneği seçtiğini bulup ona göre ipucu ver
        for opt_key, opt_data in options.items():
            if not opt_data["is_phishing"]: 
                st.session_state.last_hint = opt_data['hint']
                break 
            
    # Açıklama gösterilecek, bu yüzden hemen rerun yapma.
    # Kullanıcının "Sonraki Soru" butonuna tıklamasını bekle.
    # Ancak Streamlit'in butonları yeniden çizmesi için bir rerun gerekli.
    st.rerun() 

if not st.session_state.game_started and st.button("Oyunu Başlat"):
    st.session_state.game_started = True
    st.rerun()

if st.session_state.game_started:
    if st.session_state.question_index < len(questions):
        # Cevap verilmişse ve açıklama gösterilmesi gerekiyorsa
        if st.session_state.show_explanation:
            if st.session_state.last_answer_correct:
                st.success(f"🎉 Tebrikler! Doğru Bildiniz! Puanınız: {st.session_state.score}")
                if st.session_state.last_explanation:
                    st.markdown(f"**Neden bir oltalama girişimiydi?** 🤔 {st.session_state.last_explanation}")
            else:
                st.error(f"Yanlış cevap. 😢 Puanınız: {st.session_state.score}")
                if st.session_state.last_hint:
                    st.warning(f"**İpucu:** {st.session_state.last_hint}")
            
            # Sonraki soruya geçme butonu
            st.button("Sonraki Soru", on_click=next_question, key="next_q_button")
        else:
            # Henüz cevap verilmediyse veya açıklama gösterilmiyorsa soruyu göster
            display_question(questions[st.session_state.question_index])
    else:
        st.success(f"Tebrikler! Oyunu bitirdiniz! Toplam Puanınız: {st.session_state.score} / {len(questions) * 10}")
        st.balloons()
        st.write("Siber güvenliğiniz için SimKor her zaman yanınızda!")
        if st.button("Yeniden Oyna"):
            st.session_state.score = 0
            st.session_state.question_index = 0
            st.session_state.game_started = False 
            st.session_state.show_explanation = False
            st.session_state.last_answer_correct = False
            st.session_state.last_explanation = ""
            st.session_state.last_hint = ""
            st.rerun()

# --- Alt Bilgi ---
st.markdown("---")
st.markdown("Powered by SimKor 🛡️")