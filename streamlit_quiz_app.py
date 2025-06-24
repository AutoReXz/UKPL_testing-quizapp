import streamlit as st
import json
import os
from typing import List, Dict, Any
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="🎓 Smart Quiz App",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling yang lebih menarik
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .quiz-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e1e5e9;
        margin: 1rem 0;
    }
    
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .question-number {
        background: #667eea;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .success-badge {
        background: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
    }
    
    .error-badge {
        background: #ef4444;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
    }
    
    .stButton > button {
        border-radius: 20px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

class StreamlitQuizApp:
    def __init__(self, data_file: str = "questions.json"):
        self.data_file = data_file
        if 'questions' not in st.session_state:
            st.session_state.questions = []
            self.load_questions()
        if 'quiz_state' not in st.session_state:
            st.session_state.quiz_state = {
                'current_question': 0,
                'score': 0,
                'answers': [],
                'quiz_started': False,
                'quiz_finished': False,
                'start_time': None
            }
    
    def load_questions(self) -> None:
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    st.session_state.questions = json.load(file)
            else:
                self.create_default_questions()
        except (json.JSONDecodeError, FileNotFoundError) as e:
            st.error(f"Error loading questions: {e}")
            self.create_default_questions()
    
    def save_questions(self) -> None:
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(st.session_state.questions, file, indent=2, ensure_ascii=False)
            st.success("Questions saved successfully!")
        except Exception as e:
            st.error(f"Error saving questions: {e}")
    
    def create_default_questions(self) -> None:
        default_questions = [
            {
                "id": 1,
                "question": "Apa kepanjangan dari CPU?",
                "options": {
                    "A": "Central Processing Unit",
                    "B": "Computer Personal Unit",
                    "C": "Central Program Unit",
                    "D": "Computer Processing Unit"
                },
                "correct_answer": "A"
            },
            {
                "id": 2,
                "question": "Manakah yang merupakan bahasa pemrograman?",
                "options": {
                    "A": "HTML",
                    "B": "CSS",
                    "C": "Python",
                    "D": "HTTP"
                },
                "correct_answer": "C"
            },
            {
                "id": 3,
                "question": "Berapa hasil dari 2 + 2 * 3?",
                "options": {
                    "A": "12",
                    "B": "8",
                    "C": "10",
                    "D": "6"
                },
                "correct_answer": "B"
            },
            {
                "id": 4,
                "question": "Apa fungsi dari RAM?",
                "options": {
                    "A": "Menyimpan data permanen",
                    "B": "Memproses data",
                    "C": "Menyimpan data sementara",
                    "D": "Menampilkan data"
                },
                "correct_answer": "C"
            },
            {
                "id": 5,
                "question": "Siapa pendiri Microsoft?",
                "options": {
                    "A": "Steve Jobs",
                    "B": "Bill Gates",
                    "C": "Mark Zuckerberg",
                    "D": "Larry Page"
                },
                "correct_answer": "B"
            }        ]
        st.session_state.questions = default_questions
        self.save_questions()
    
    def reset_quiz(self):
        st.session_state.quiz_state = {
            'current_question': 0,
            'score': 0,
            'answers': [],
            'quiz_started': False,
            'quiz_finished': False,
            'start_time': None
        }
    
    def start_quiz_page(self):
        # Header dengan styling yang menarik
        st.markdown("""
        <div class="main-header">
            <h1>🎓 Smart Quiz Application</h1>
            <p>Tingkatkan pengetahuan Anda dengan quiz interaktif</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.questions:
            st.error("❌ Tidak ada soal tersedia. Silakan tambah soal di menu 'Kelola Soal'.")
            return
        
        if not st.session_state.quiz_state['quiz_started']:
            # Dashboard info
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="📊 Total Soal",
                    value=len(st.session_state.questions),
                    help="Jumlah soal yang tersedia"
                )
                
            with col2:
                estimated_time = len(st.session_state.questions) * 1.5  # 1.5 menit per soal
                st.metric(
                    label="⏱️ Estimasi Waktu",
                    value=f"{estimated_time:.0f} menit",
                    help="Perkiraan waktu untuk menyelesaikan quiz"
                )
                
            with col3:
                st.metric(
                    label="🎯 Target Nilai",
                    value="80%",
                    help="Target nilai untuk kategori 'Sangat Baik'"
                )
            
            st.markdown("---")
            
            # Instructions dengan design yang menarik
            st.markdown("""
            <div class="quiz-card">
                <h3>📋 Petunjuk Quiz</h3>
                <ul>
                    <li>✅ Baca setiap pertanyaan dengan teliti</li>
                    <li>🎯 Pilih jawaban yang paling tepat dari 4 pilihan</li>
                    <li>➡️ Gunakan tombol navigasi untuk berpindah soal</li>
                    <li>💾 Jawaban akan tersimpan otomatis</li>
                    <li>📊 Hasil dan analisis ditampilkan di akhir</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Start button dengan animation
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("🚀 Mulai Quiz Sekarang", type="primary", use_container_width=True):
                    st.session_state.quiz_state['quiz_started'] = True
                    st.session_state.quiz_state['start_time'] = time.time()
                    st.balloons()  # Animasi balon
                    st.rerun()
        
        elif st.session_state.quiz_state['quiz_finished']:
            self.show_results()
        
        else:
            self.show_quiz_question()
    
    def show_quiz_question(self):
        current_q = st.session_state.quiz_state['current_question']
        total_q = len(st.session_state.questions)
        question = st.session_state.questions[current_q]
        
        # Progress bar
        progress = (current_q + 1) / total_q
        st.progress(progress)
        st.markdown(f"**Soal {current_q + 1} dari {total_q}**")
        
        # Question
        st.markdown(f"### {question['question']}")
        
        # Options
        answer = st.radio(
            "Pilih jawaban:",
            options=list(question['options'].keys()),
            format_func=lambda x: f"{x}. {question['options'][x]}",
            key=f"question_{current_q}"
        )
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1,1,1])
        
        with col1:
            if current_q > 0:
                if st.button("← Previous"):
                    st.session_state.quiz_state['current_question'] -= 1
                    st.rerun()
        
        with col3:
            if answer:
                if current_q < total_q - 1:
                    if st.button("Next →", type="primary"):
                        # Save answer
                        if len(st.session_state.quiz_state['answers']) <= current_q:
                            st.session_state.quiz_state['answers'].append(answer)
                        else:
                            st.session_state.quiz_state['answers'][current_q] = answer
                        
                        st.session_state.quiz_state['current_question'] += 1
                        st.rerun()
                else:
                    if st.button("🏁 Finish Quiz", type="primary"):
                        # Save final answer
                        if len(st.session_state.quiz_state['answers']) <= current_q:
                            st.session_state.quiz_state['answers'].append(answer)
                        else:
                            st.session_state.quiz_state['answers'][current_q] = answer                        
                        # Calculate score
                        score = 0
                        for i, user_answer in enumerate(st.session_state.quiz_state['answers']):
                            if user_answer == st.session_state.questions[i]['correct_answer']:
                                score += 1
                        
                        st.session_state.quiz_state['score'] = score
                        st.session_state.quiz_state['quiz_finished'] = True
                        st.rerun()
    
    def show_results(self):
        # Header hasil yang menarik
        st.markdown("""
        <div class="main-header">
            <h1>🎉 Hasil Quiz Anda</h1>
            <p>Selamat! Anda telah menyelesaikan quiz</p>
        </div>
        """, unsafe_allow_html=True)
        
        score = st.session_state.quiz_state['score']
        total = len(st.session_state.questions)
        percentage = (score / total) * 100
        
        # Hitung waktu yang dihabiskan
        if st.session_state.quiz_state.get('start_time'):
            elapsed_time = time.time() - st.session_state.quiz_state['start_time']
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            time_text = f"{minutes}m {seconds}s"
        else:
            time_text = "N/A"
        
        # Metrics dengan styling yang menarik
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Skor Anda",
                value=f"{score}/{total}",
                help="Jumlah jawaban benar dari total soal"
            )
            
        with col2:
            st.metric(
                label="📈 Persentase",
                value=f"{percentage:.1f}%",
                delta=f"{percentage-75:.1f}% dari target",
                help="Persentase keberhasilan Anda"
            )
            
        with col3:
            if percentage >= 80:
                grade = "Sangat Baik! 🎉"
                color = "green"
            elif percentage >= 60:
                grade = "Baik 👍"
                color = "blue"
            elif percentage >= 40:
                grade = "Cukup 😊"
                color = "orange"
            else:
                grade = "Perlu Belajar 📚"
                color = "red"
                
            st.metric(
                label="🏆 Kategori",
                value=grade,
                help="Kategori berdasarkan persentase nilai"
            )
            
        with col4:
            st.metric(
                label="⏱️ Waktu",
                value=time_text,
                help="Total waktu yang dihabiskan"
            )
        
        # Visualisasi hasil dengan chart
        st.markdown("---")
        st.markdown("### 📊 Analisis Hasil")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart untuk distribusi jawaban
            correct_count = score
            incorrect_count = total - score
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Benar', 'Salah'],
                values=[correct_count, incorrect_count],
                hole=.3,
                marker_colors=['#10b981', '#ef4444']
            )])
            fig_pie.update_layout(
                title="Distribusi Jawaban",
                font_size=14,
                showlegend=True
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart perbandingan dengan kategori
            categories = ['Perlu Belajar', 'Cukup', 'Baik', 'Sangat Baik']
            thresholds = [40, 60, 80, 100]
            colors = ['red' if percentage < 40 else 
                     'orange' if percentage < 60 else 
                     'blue' if percentage < 80 else 'green' 
                     for _ in thresholds]
            
            fig_bar = go.Figure(data=[
                go.Bar(x=categories, y=thresholds, 
                      marker_color=['lightgray']*4,
                      name='Target'),
                go.Bar(x=[categories[min(3, int(percentage//20))]], 
                      y=[percentage], 
                      marker_color=color,
                      name='Skor Anda')
            ])
            fig_bar.update_layout(
                title="Posisi Skor Anda",
                yaxis_title="Persentase (%)",
                showlegend=True
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Detail jawaban dengan styling yang lebih menarik
        st.markdown("---")
        st.markdown("### � Review Jawaban Detail")
        
        correct_answers = []
        incorrect_answers = []
        
        for i, question in enumerate(st.session_state.questions):
            user_answer = st.session_state.quiz_state['answers'][i]
            correct_answer = question['correct_answer']
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_answers.append(i+1)
            else:
                incorrect_answers.append(i+1)
        
        # Summary boxes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #10b981, #059669); 
                        color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                <h4>✅ Jawaban Benar</h4>
                <p>{}</p>
                <p>Soal nomor: {}</p>
            </div>
            """.format(
                f"{len(correct_answers)} dari {total} soal",
                ", ".join(map(str, correct_answers)) if correct_answers else "Tidak ada"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ef4444, #dc2626); 
                        color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                <h4>❌ Jawaban Salah</h4>
                <p>{}</p>
                <p>Soal nomor: {}</p>
            </div>
            """.format(
                f"{len(incorrect_answers)} dari {total} soal",
                ", ".join(map(str, incorrect_answers)) if incorrect_answers else "Tidak ada"
            ), unsafe_allow_html=True)
        
        # Detail setiap soal
        for i, question in enumerate(st.session_state.questions):
            user_answer = st.session_state.quiz_state['answers'][i]
            correct_answer = question['correct_answer']
            is_correct = user_answer == correct_answer
            
            status_icon = "✅" if is_correct else "❌"
            status_color = "green" if is_correct else "red"
            
            with st.expander(f"{status_icon} Soal {i+1}: {question['question']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Jawaban Anda:**")
                    st.markdown(f"**{user_answer}.** {question['options'][user_answer]}")
                    
                with col2:
                    st.markdown("**Jawaban Benar:**")
                    st.markdown(f"**{correct_answer}.** {question['options'][correct_answer]}")
                
                if is_correct:
                    st.success("🎉 Benar! Anda menjawab dengan tepat.")
                else:
                    st.error("💡 Jawaban yang benar adalah option " + correct_answer)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1,1,1])
        
        with col1:
            if st.button("🔄 Coba Lagi", type="secondary", use_container_width=True):
                self.reset_quiz()
                st.rerun()
                
        with col2:
            if st.button("📊 Lihat Statistik", type="secondary", use_container_width=True):
                st.info("Fitur statistik akan segera tersedia!")
                
        with col3:
            if st.button("🏠 Kembali ke Home", type="primary", use_container_width=True):
                self.reset_quiz()
                st.rerun()
    
    def manage_questions_page(self):
        st.title("⚙️ Kelola Soal")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Daftar Soal", "➕ Tambah Soal", "✏️ Edit Soal", "🗑️ Hapus Soal"])
        
        with tab1:
            self.display_questions()
        
        with tab2:
            self.add_question_form()
        
        with tab3:
            self.edit_question_form()
        
        with tab4:
            self.delete_question_form()
    
    def display_questions(self):
        if not st.session_state.questions:
            st.info("Tidak ada soal tersedia.")
            return
        
        for i, question in enumerate(st.session_state.questions):
            with st.expander(f"ID {question['id']}: {question['question']}", expanded=False):
                for option, text in question['options'].items():
                    if option == question['correct_answer']:
                        st.markdown(f"**{option}. {text} ✅**")
                    else:
                        st.markdown(f"{option}. {text}")
    
    def add_question_form(self):
        with st.form("add_question"):
            st.markdown("### Tambah Soal Baru")
            
            question_text = st.text_area("Soal:", placeholder="Masukkan pertanyaan...")
            
            col1, col2 = st.columns(2)
            with col1:
                option_a = st.text_input("Pilihan A:", placeholder="Pilihan A")
                option_c = st.text_input("Pilihan C:", placeholder="Pilihan C")
            with col2:
                option_b = st.text_input("Pilihan B:", placeholder="Pilihan B")
                option_d = st.text_input("Pilihan D:", placeholder="Pilihan D")
            
            correct_answer = st.selectbox("Jawaban yang benar:", ["A", "B", "C", "D"])
            
            submitted = st.form_submit_button("➕ Tambah Soal", type="primary")
            
            if submitted:
                if not all([question_text, option_a, option_b, option_c, option_d]):
                    st.error("Semua field harus diisi!")
                else:
                    new_id = max([q['id'] for q in st.session_state.questions], default=0) + 1
                    new_question = {
                        "id": new_id,
                        "question": question_text,
                        "options": {
                            "A": option_a,
                            "B": option_b,
                            "C": option_c,
                            "D": option_d
                        },
                        "correct_answer": correct_answer
                    }
                    st.session_state.questions.append(new_question)
                    self.save_questions()
                    st.success("✅ Soal berhasil ditambahkan!")
                    st.rerun()
    
    def edit_question_form(self):
        if not st.session_state.questions:
            st.info("Tidak ada soal untuk diedit.")
            return
        
        # Select question to edit
        question_options = {f"ID {q['id']}: {q['question'][:50]}...": q['id'] for q in st.session_state.questions}
        selected_question = st.selectbox("Pilih soal yang ingin diedit:", list(question_options.keys()))
        
        if selected_question:
            question_id = question_options[selected_question]
            question_index = next(i for i, q in enumerate(st.session_state.questions) if q['id'] == question_id)
            question = st.session_state.questions[question_index]
            
            with st.form("edit_question"):
                st.markdown(f"### Edit Soal ID: {question_id}")
                
                question_text = st.text_area("Soal:", value=question['question'])
                
                col1, col2 = st.columns(2)
                with col1:
                    option_a = st.text_input("Pilihan A:", value=question['options']['A'])
                    option_c = st.text_input("Pilihan C:", value=question['options']['C'])
                with col2:
                    option_b = st.text_input("Pilihan B:", value=question['options']['B'])
                    option_d = st.text_input("Pilihan D:", value=question['options']['D'])
                
                correct_answer = st.selectbox("Jawaban yang benar:", ["A", "B", "C", "D"], 
                                            index=["A", "B", "C", "D"].index(question['correct_answer']))
                
                submitted = st.form_submit_button("💾 Simpan Perubahan", type="primary")
                
                if submitted:
                    if not all([question_text, option_a, option_b, option_c, option_d]):
                        st.error("Semua field harus diisi!")
                    else:
                        st.session_state.questions[question_index] = {
                            "id": question_id,
                            "question": question_text,
                            "options": {
                                "A": option_a,
                                "B": option_b,
                                "C": option_c,
                                "D": option_d
                            },
                            "correct_answer": correct_answer
                        }
                        self.save_questions()
                        st.success("✅ Soal berhasil diedit!")
                        st.rerun()
    
    def delete_question_form(self):
        if not st.session_state.questions:
            st.info("Tidak ada soal untuk dihapus.")
            return
        
        st.markdown("### Hapus Soal")
        st.warning("⚠️ Perhatian: Tindakan ini tidak dapat dibatalkan!")
        
        # Select question to delete
        question_options = {f"ID {q['id']}: {q['question'][:50]}...": q['id'] for q in st.session_state.questions}
        selected_question = st.selectbox("Pilih soal yang ingin dihapus:", list(question_options.keys()))
        
        if selected_question:
            question_id = question_options[selected_question]
            question = next(q for q in st.session_state.questions if q['id'] == question_id)
            
            with st.expander("Preview soal yang akan dihapus:", expanded=True):
                st.markdown(f"**{question['question']}**")
                for option, text in question['options'].items():
                    if option == question['correct_answer']:
                        st.markdown(f"**{option}. {text} ✅**")
                    else:
                        st.markdown(f"{option}. {text}")
            
            col1, col2, col3 = st.columns([1,1,1])
            with col2:
                if st.button("🗑️ Hapus Soal", type="primary", use_container_width=True):
                    st.session_state.questions = [q for q in st.session_state.questions if q['id'] != question_id]
                    self.save_questions()
                    st.success("✅ Soal berhasil dihapus!")
                    st.rerun()

def main():
    app = StreamlitQuizApp()
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🎯 Quiz App")
        st.markdown("---")
        
        page = st.radio(
            "Navigasi:",
            ["🏠 Beranda", "📚 Mulai Quiz", "⚙️ Kelola Soal"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📊 Statistik")
        if st.session_state.questions:
            st.metric("Total Soal", len(st.session_state.questions))
        else:
            st.metric("Total Soal", 0)
        
        if st.session_state.quiz_state['quiz_finished']:
            st.metric("Skor Terakhir", f"{st.session_state.quiz_state['score']}/{len(st.session_state.questions)}")
    
    # Main content
    if page == "🏠 Beranda":
        st.title("🎯 Selamat Datang di Quiz App")
        st.markdown("### Aplikasi quiz interaktif dengan antarmuka yang mudah digunakan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌟 Fitur Utama:")
            st.markdown("- 📚 Quiz pilihan ganda interaktif")
            st.markdown("- ⚙️ Kelola soal (tambah, edit, hapus)")
            st.markdown("- 📊 Tracking skor dan progress")
            st.markdown("- 🎨 Interface yang user-friendly")
            st.markdown("- 💾 Penyimpanan data otomatis")
        
        with col2:
            st.markdown("#### 🚀 Cara Penggunaan:")
            st.markdown("1. **Mulai Quiz** - Klik untuk memulai quiz")
            st.markdown("2. **Kelola Soal** - Tambah/edit soal")
            st.markdown("3. **Lihat Hasil** - Cek skor dan jawaban")
            st.markdown("4. **Ulangi** - Coba lagi untuk skor lebih baik")
        
        st.markdown("---")
        st.info("💡 Tips: Gunakan sidebar untuk navigasi antar halaman")
    
    elif page == "📚 Mulai Quiz":
        app.start_quiz_page()
    
    elif page == "⚙️ Kelola Soal":
        app.manage_questions_page()

if __name__ == "__main__":
    main()
