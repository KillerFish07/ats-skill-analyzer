from rapidfuzz import fuzz

def match_skills(jd_skills, resume_section_skills):
    # Accepts both dict and flat list
    if isinstance(resume_section_skills, dict):
        resume_skills_all = [skill for skills in resume_section_skills.values() for skill in skills]
    elif isinstance(resume_section_skills, list):
        resume_skills_all = resume_section_skills
    else:
        resume_skills_all = []

    matched = []
    missing = []

    for jd_skill in jd_skills:
        found = False
        for resume_skill in resume_skills_all:
            if fuzz.partial_ratio(jd_skill.lower(), resume_skill.lower()) > 80:
                matched.append(jd_skill)
                found = True
                break
        if not found:
            missing.append(jd_skill)

    score = round((len(matched) / len(jd_skills)) * 100, 2) if jd_skills else 0.0

    return matched, missing, score
