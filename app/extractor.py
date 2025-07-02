import spacy
import re
from rapidfuzz import fuzz

class SkillExtractor:
    def __init__(self, skills_list, synonyms_map=None, use_fuzzy=False):
        self.skills = set(skill.lower() for skill in skills_list)
        self.synonyms = synonyms_map if synonyms_map else {}
        self.use_fuzzy = use_fuzzy
        self.nlp = spacy.load("en_core_web_sm")

    def normalize(self, skill):
        skill = skill.lower().strip()
        return self.synonyms.get(skill, skill)

    def extract(self, text):
        if not text: return []
        text = text.lower()
        words = set(re.findall(r'\b\w[\w-]+\b', text))
        found = set()

        for word in words:
            word = self.normalize(word)
            if word in self.skills:
                found.add(word)
            elif self.use_fuzzy:
                for skill in self.skills:
                    if fuzz.ratio(word, skill) > 85:
                        found.add(skill)
        return sorted(found)

    def extract_section_wise(self, text):
        sections = {
            'education': r'(education|academic).*?(?=(experience|projects|skills|certifications|$))',
            'experience': r'(experience|work).*?(?=(education|projects|skills|certifications|$))',
            'projects': r'(projects).*?(?=(education|experience|skills|certifications|$))',
            'skills': r'(skills|technologies).*?(?=(education|projects|experience|certifications|$))',
            'certifications': r'(certifications|licenses).*?(?=(education|projects|experience|skills|$))',
            'summary': r'(summary|objective|profile).*?(?=(education|projects|experience|skills|certifications|$))'
        }

        result = {}
        for section, pattern in sections.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                section_text = match.group(0)
                extracted = self.extract(section_text)
                if extracted:
                    result[section] = extracted
        return result
