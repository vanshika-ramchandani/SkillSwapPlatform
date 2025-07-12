from app import create_app, db
from app.models import Skill

app = create_app()

skills = [
    "Python", "Java", "C++", "JavaScript", "TypeScript", "HTML/CSS", "SQL",
    "NoSQL", "MongoDB", "React", "Vue.js", "Node.js", "Django", "Flask", "Spring Boot",
    "Git/GitHub", "DevOps", "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud",
    "Firebase", "Linux", "Shell Scripting", "Machine Learning", "Deep Learning",
    "Data Science", "Data Analysis", "Power BI", "Tableau", "Excel", "Word",
    "Photoshop", "Canva", "Figma", "Illustrator", "UI/UX Design", "Graphic Design",
    "Video Editing", "Adobe Premiere", "After Effects", "Photography", "3D Modeling",
    "AutoCAD", "Blender", "Unity", "Game Development", "Cybersecurity",
    "Ethical Hacking", "Network Security", "Penetration Testing", "Cloud Computing",
    "Blockchain", "Cryptography", "Arduino", "Raspberry Pi", "IoT", "Embedded Systems",
    "Public Speaking", "Communication", "Time Management", "Leadership", "Teamwork",
    "Project Management", "Agile", "Scrum", "JIRA", "Business Analysis", "Problem Solving",
    "Critical Thinking", "Negotiation", "Sales", "Digital Marketing", "SEO", "SEM",
    "Content Writing", "Blogging", "Copywriting", "Creative Writing", "Technical Writing",
    "Tutoring", "Teaching", "Translation", "Language Proficiency", "Spanish", "French",
    "German", "Hindi", "Mandarin", "Cooking", "Baking", "Guitar", "Piano", "Singing",
    "Drawing", "Painting", "Yoga", "Fitness Training", "Career Coaching", "Resume Writing",
    "Event Planning", "Customer Service", "Research", "Others"
]

with app.app_context():
    for name in skills:
        if not Skill.query.filter_by(name=name).first():
            db.session.add(Skill(name=name))
    db.session.commit()
    print("Added 100+ skills including 'Others' to Skill table.")
