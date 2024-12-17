<h1 align="center">🎬 A Hybrid Movie Recommendation System Leveraging KNN and TF-IDF</h1>

## <h2>📌 Overview</h2>
<p>
This project is a <strong>hybrid movie recommendation system</strong> that combines 
<strong>K-Nearest Neighbors (KNN)</strong> and <strong>TF-IDF</strong> techniques to deliver personalized movie recommendations. 
The system utilizes movie metadata like plot summaries, genres, and other attributes to find movies similar to user preferences.
</p>
<p>🚀 The project is deployed and live here: 
<a href="https://movie-recommendation-system-z32q.onrender.com" target="_blank">Movie Recommendation System</a>.</p>

---

## <h2>🚀 Features</h2>
<ul>
  <li><strong>Content-Based Filtering</strong>: Leverages TF-IDF to analyze movie plot summaries and identify important keywords.</li>
  <li><strong>Similarity Matching</strong>: Implements KNN to compute similarities between movies based on extracted TF-IDF features.</li>
  <li><strong>Hybrid Approach</strong>: Combines content-based and collaborative techniques for accurate and diverse recommendations.</li>
  <li><strong>User-Friendly Interface</strong>: A simple web-based interface to input movies and view recommendations.</li>
</ul>

---

## <h2>🔧 Technologies Used</h2>
<ul>
  <li><strong>Python</strong>: Core programming language.</li>
  <li><strong>Machine Learning</strong>: K-Nearest Neighbors (KNN) algorithm.</li>
  <li><strong>NLP Techniques</strong>: TF-IDF (Term Frequency-Inverse Document Frequency) for text feature extraction.</li>
  <li><strong>Libraries</strong>:
    <ul>
      <li><code>pandas</code> and <code>numpy</code> - Data manipulation</li>
      <li><code>scikit-learn</code> - Machine learning algorithms and TF-IDF</li>
      <li><code>Flask</code> - Backend framework for deployment</li>
      <li><code>HTML/CSS</code> - Frontend interface</li>
    </ul>
  </li>
  <li><strong>Deployment</strong>: Hosted on <a href="https://render.com" target="_blank">Render</a>.</li>
</ul>

---

## <h2>📊 How It Works</h2>
<ol>
  <li><strong>Data Preprocessing</strong>:
    <ul>
      <li>Movie metadata (title, plot, genres) is cleaned and processed.</li>
      <li>TF-IDF transforms movie plots into numerical vectors, highlighting key terms.</li>
    </ul>
  </li>
  <li><strong>Similarity Computation</strong>:
    <ul>
      <li>KNN computes similarity scores between movies using cosine similarity.</li>
      <li>The system identifies movies closest to the user-selected movie(s).</li>
    </ul>
  </li>
  <li><strong>Recommendations</strong>: 
    Based on the similarity scores, the top <em>N</em> most relevant movies are recommended.
  </li>
</ol>

---

## <h2>🛠️ Setup Instructions</h2>
<ol>
  <li><strong>Clone the Repository</strong>:</li>
  <pre><code>git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system</code></pre>
  
  <li><strong>Install Dependencies</strong>:</li>
  <pre><code>pip install -r requirements.txt</code></pre>
  
  <li><strong>Run the Application</strong>:</li>
  <pre><code>python app.py</code></pre>
  <p>Open your browser and go to <a href="http://127.0.0.1:5000/">http://127.0.0.1:5000/</a>.</p>
</ol>

---

## <h2>💻 Demo</h2>
<p>
Check out the live project here: 
<a href="https://movie-recommendation-system-z32q.onrender.com" target="_blank">Movie Recommendation System</a>.
</p>

---

## <h2>📈 Future Improvements</h2>
<ul>
  <li>Integrate collaborative filtering for user-based recommendations.</li>
  <li>Add movie ratings and user reviews for enhanced recommendations.</li>
  <li>Implement advanced clustering techniques like K-Means for better categorization.</li>
  <li>Improve the user interface with interactive visuals.</li>
</ul>

---

## <h2>🤝 Contributions</h2>
<p>Feel free to fork this repository, open issues, or submit pull requests for any enhancements!</p>

---

## <h2>📄 License</h2>
<p>This project is open-source and available under the <strong>MIT License</strong>.</p>

---

## <h2>📧 Contact</h2>
<p>
<strong>Your Name</strong>: [Your Email]<br>
<strong>GitHub</strong>: <a href="https://github.com/your-username" target="_blank">https://github.com/your-username</a>
</p>
