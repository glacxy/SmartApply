import pymupdf
import re


# Extract text from PDF
def extract_text_from_pdf(file_bytes: bytes) -> str:

    pdf_document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    )

    extracted_text = ""

    for page in pdf_document:
        extracted_text += page.get_text()

    pdf_document.close()

    return extracted_text


# Extract email
def extract_email(text: str):

    pattern = r'[\w.-]+@[\w.-]+\.\w+'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


# Extract phone number
def extract_phone(text: str):

    pattern = r'(?<!\d)(?:\+91[-\s]?)?[6-9]\d{9}(?!\d)'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


# Extract name (first non-empty line)
def extract_name(text: str):

    lines = text.strip().splitlines()

    for line in lines:
        line = line.strip()

        if line and not re.search(r'@|https?://|www\.|^\+?\d', line):
            return line

    return None


# Extract skills from resume
def extract_skills(text: str):

    known_skills = [
        "Python", "Java", "C++", "JavaScript",
        "React", "React.js", "Node.js", "Express.js",
        "FastAPI", "Spring Boot", "MongoDB", "MySQL",
        "Docker", "AWS", "Git", "GitHub",
        "HTML", "CSS", "Bootstrap", "REST APIs",
        "Machine Learning", "Deep Learning", "RAG",
        "LLM", "Linux", "C", "Redis",
        "Socket.IO", "Maven", "React Native"
    ]

    found_skills = []

    for skill in known_skills:
        if re.search(
            r'(?<!\w)' + re.escape(skill) + r'(?!\w)',
            text,
            re.IGNORECASE
        ):
            found_skills.append(skill)

    return found_skills


# Extract section text using headings
def extract_section(text: str, section_names: list):

    lines = text.splitlines()

    collecting = False
    section_content = []

    all_headings = [
        "EDUCATION", "EXPERIENCE", "WORK EXPERIENCE",
        "PROJECTS", "TECHNICAL SKILLS", "SKILLS",
        "CERTIFICATIONS", "ACHIEVEMENTS",
        "COMPETITIVE PROGRAMMING"
    ]

    for line in lines:

        cleaned_line = line.strip().upper()

        # Start collecting when target section is found
        if cleaned_line in section_names:
            collecting = True
            continue

        # Stop when another section heading is found
        if collecting and cleaned_line in all_headings:
            break

        if collecting:
            section_content.append(line.strip())

    return "\n".join(section_content).strip() or None


# Build structured resume JSON
def parse_resume(text: str):

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_section(
            text, ["EDUCATION"]
        ),
        "experience": extract_section(
            text, ["EXPERIENCE", "WORK EXPERIENCE"]
        ),
        "projects": extract_section(
            text, ["PROJECTS"]
        )
    }
