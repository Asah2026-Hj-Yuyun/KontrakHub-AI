from __future__ import annotations

import re
import unicodedata

def cleaningText(text):
    text = unicodedata.normalize('NFKD', str(text))
    text = ''.join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'[0-9]+', ' angka ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'(.)\1{3,}', r'\1\1\1', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def casefoldingText(text):
    return text.lower()

def tokenizingText(text):
    return text.split()

listStopwords = {
    'iya', 'yaa', 'ya', 'sih', 'loh', 'kah', 'dong', 'woi', 'woii', 'woy',
    'teh', 'atuh', 'mah', 'euy', 'weh', 'nya',
}

def filteringText(tokens):
    return [t for t in tokens if t not in listStopwords]

def toSentence(tokens):
    return ' '.join(tokens)

slangwords = {
    # Indonesia
    'gak': 'nggak', 'ga': 'nggak', 'gk': 'nggak', 'engga': 'nggak', 'enggak': 'nggak',
    'tdk': 'nggak', 'brp': 'berapa', 'sebln': 'sebulan', 'sbln': 'sebulan',
    'tgl': 'tanggal', 'yg': 'yang', 'udah': 'sudah', 'udh': 'sudah', 'sdh': 'sudah',
    'blm': 'belum', 'belom': 'belum', 'dmn': 'dimana', 'kpn': 'kapan',
    'bgmn': 'bagaimana', 'gmn': 'bagaimana', 'gimana': 'bagaimana',
    'bs': 'bisa', 'tlg': 'tolong', 'kk': 'kak', 'sy': 'saya', 'aku': 'saya',
    'kmr': 'kamar', 'byr': 'bayar', 'pmbyrn': 'pembayaran', 'listrk': 'listrik',
    # Sunda
    'sbrh': 'sabaraha', 'kmh': 'kumaha', 'teu': 'henteu',
    'abi': 'abdi', 'atos': 'geus', 'tos': 'geus', 'nu': 'anu',
    'hatur': 'nuhun', 'mayar': 'bayar',
}

def fix_slangwords(text):
    return ' '.join(slangwords.get(w, w) for w in text.split())

def clean_text(text):
    text = cleaningText(text)
    text = casefoldingText(text)
    text = fix_slangwords(text)
    text = filteringText(tokenizingText(text))
    return toSentence(text)