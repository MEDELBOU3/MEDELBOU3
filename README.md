<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary-color: #00F7E2;
            --secondary-color: #FF4470;
            --bg-dark: #0D1117;
            --text-light: #F0F6FC;
            --card-bg: #161B22;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'JetBrains Mono', monospace;
            background: var(--bg-dark);
            color: var(--text-light);
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .hero-section {
            text-align: center;
            padding: 50px 0;
            background: linear-gradient(135deg, rgba(13,17,23,0.95) 0%, rgba(22,27,34,0.95) 100%);
            border-radius: 15px;
            margin-bottom: 30px;
        }

        .hero-title {
            font-size: 2.5em;
            margin-bottom: 20px;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: titleGlow 2s ease-in-out infinite;
        }

        .social-links {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
            margin: 20px 0;
        }

        .social-links a {
            transition: transform 0.3s ease;
        }

        .social-links a:hover {
            transform: translateY(-5px);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .stats-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }

        .stats-card:hover {
            transform: translateY(-5px);
        }

        .skills-section {
            margin: 40px 0;
        }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .skill-item {
            background: var(--card-bg);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .skill-item:hover {
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            transform: scale(1.05);
        }

        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .project-card {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 20px;
            transition: transform 0.3s ease;
        }

        .project-card:hover {
            transform: translateY(-5px);
        }

        .contact-form {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: var(--card-bg);
            border-radius: 10px;
        }

        .contact-form input,
        .contact-form textarea {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid var(--primary-color);
            background: var(--bg-dark);
            color: var(--text-light);
        }

        .button {
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            color: var(--bg-dark);
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: transform 0.3s ease;
        }

        .button:hover {
            transform: scale(1.05);
        }

        @keyframes titleGlow {
            0%, 100% {
                text-shadow: 0 0 10px rgba(0,247,226,0.5);
            }
            50% {
                text-shadow: 0 0 20px rgba(0,247,226,0.8);
            }
        }

        @media (max-width: 768px) {
            .hero-title {
                font-size: 2em;
            }
            .stats-grid {
                grid-template-columns: 1fr;
            }
            .social-links {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <section class="hero-section">
            <h1 class="hero-title">Mohamed EL-bouanani</h1>
            <div class="typing-animation">
                <img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&pause=1000&color=00F7E2&center=true&vCenter=true&random=false&width=435&lines=Computer+Science+%26+AI+Student;Full-Stack+Developer;Machine+Learning+Enthusiast;Always+learning+new+things" alt="Typing SVG" />
            </div>
        </section>

        <div class="social-links">
            <a href="https://www.facebook.com/Simo.lbou3" target="_blank" rel="noopener noreferrer">
                <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"/>
            </a>
            <a href="https://instagram.com/simo_elb_3" target="_blank" rel="noopener noreferrer">
                <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram"/>
            </a>
            <a href="https://www.youtube.com/@digitalvortex203" target="_blank" rel="noopener noreferrer">
                <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"/>
            </a>
        </div>

        <div class="stats-grid">
            <div class="stats-card">
                <h3>GitHub Stats</h3>
                <img src="https://github-readme-stats.vercel.app/api?username=MEDELBOU3&show_icons=true&theme=radical" alt="GitHub Stats" width="100%">
            </div>
            <div class="stats-card">
                <h3>Top Languages</h3>
                <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=MEDELBOU3&layout=compact&theme=radical" alt="Top Languages" width="100%">
            </div>
        </div>

        <section class="skills-section">
            <h2>🛠️ Skills & Technologies</h2>
            <div class="skills-grid">
                <div class="skill-item">Python</div>
                <div class="skill-item">JavaScript</div>
                <div class="skill-item">React</div>
                <div class="skill-item">TensorFlow</div>
                <div class="skill-item">Node.js</div>
                <div class="skill-item">MongoDB</div>
            </div>
        </section>

        <section class="projects-grid">
            <div class="project-card">
                <h3>AI-Powered Healthcare</h3>
                <p>A revolutionary healthcare solution using artificial intelligence.</p>
                <a href="#" class="button">Learn More</a>
            </div>
            <div class="project-card">
                <h3>Blockchain Voting System</h3>
                <p>Secure and transparent voting system using blockchain technology.</p>
                <a href="#" class="button">Learn More</a>
            </div>
        </section>

        <section class="contact-form">
            <h2>📫 Get in Touch</h2>
            <form>
                <input type="text" placeholder="Name" required>
                <input type="email" placeholder="Email" required>
                <textarea placeholder="Message" rows="5" required></textarea>
                <button type="submit" class="button">Send Message</button>
            </form>
        </section>
    </div>

    <script>
        // Add smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Add intersection observer for animation
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        });

        document.querySelectorAll('.stats-card, .skill-item, .project-card').forEach((el) => observer.observe(el));
    </script>
</body>
</html>




