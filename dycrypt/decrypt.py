from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate, PageBreak, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from string import ascii_uppercase
from collections import Counter
import numpy as np
import string

# Cipher Text
cipher_text = """LAVHEBSJMDINFGXCLWTUUWARWBQWFTEHWUDDTCAAKKTXTSMYALMVHTAHJHKICFAFZKLEXA
TXIXYMFVLVGUDALRFJTTGKXNLOYOWLVVVQAFKVGEZLEHEXHEZGPVZEDOWARZEAFSGVASOS
DXJIEZESBEWTDWSFGVOPMUMJENPKWKMMCQKVXJMGZWVBEEWMQLARXGUNWLLWEDKKHCICAF
LKFPOHWJTTGEEKLHKLEUJVTKEAESJXJYLFDSPVRFAJUXDINFAKLFQEFAEXJYNMTDXKSRQU
GOVVTTWUHEXEZLGYVPEOLJHEMCOGEFLRIOSLBFRSRJGFKLEFWUAESLAYQIISVUVWKVZEZA
FKVWPAFKXKSAOGMKKSRPWJHIHUXQSNKLODARXUAADJSGKMSEMWWSCARWVXIELVMVZVJODW
PTDTLQESGPGOYEMGZGAFAGGJWEDNAVVWNAOWGTVYBLUXIXAUFUHDQUZAUTKMOZKTRUIFMM
DMNMTTLZXBIYZWUXJWADQLHUICDQHMKLEOGEFLRIOSLBFRSEGDXCCIZLZXYENPKGYKLEQF
VNJIRFZALRTPXAWLSSTTOZXEXHQVSMRMSUFEHKMOZGNXIILQULKFRIOFWMNSRWKGKRXRQK
LHEENQDWVKVOZAUWVZIOWAYKLEOGEFLRIOSLBFRSBJGOZHEDAKLVVVQVOBKLAISJKRRTEW
WDZRGFZGLVGOYEMGZGAFAGGJXHQHJHMMDQJUTEROFHJHMMDQLZXUETMTWVRYSQALARWDQK
AZEIDFZWMVGHZGDHXCSGUZMYETULUTEROFTWTTGEEKWWSCAZQLAZVDBSJMPAEPGFHKLAHW
SGPWIXNWKSYLXWLLRRDFZWWZWCGKKBFRSIALAZRTTWWQVGUFANXSVAZUZTIISFADEFRGAA
FZNLIXWLAVVETSKGFXYQLTXVRAPWUBJMOZOZXKLEDLGLVIKXWYBJPAFAGGNIMGKLPFVKIA
LATSNSJWLJMNPMKMICAOSVXDMCEHJBMECKYJHLTSMFVHKLEDKLHTVARLSGRTPDGSVYXHML
SWUVEEKWLRPLAXLAVQUXLAICICAEHXKMNSUGGTIRZKLARXHMNWUVINFZWYFGUEGXLFQUOZ
VXSETQTMMNICMFSECEGDWWMYETIWOBCPNQWVHEKOUFYAFREELSGUMNRGJFVHPGTDBTHENS
LXRFOGLZHNFEELLHGVOFWUMCMBQJLRRRDEWUNIMTKAFUFXHAMJERASMFVHLVTQUZGFPOSQ"""

cipher_text = cipher_text.replace("\n", "").replace(" ", "")

def index_of_coincidence(cipher_text, m):
    """
    Calculate the index of coincidence for each substring of the cipher text
    for a given keyword length m.

    Parameters:
    - cipher_text: str. The cipher text from which to calculate the IC.
    - m: int. The guessed keyword length.

    Returns:
    A list containing the index of coincidence for each substring.
    """
    # Split the cipher text into m substrings
    substrings = ['' for _ in range(m)]
    for i, char in enumerate(cipher_text):
        substrings[i % m] += char

    # Function to calculate the IC of a single substring
    def calculate_ic(substring):
        N = len(substring)
        frequency = Counter(substring)
        ic = sum(f*(f-1) for f in frequency.values()) / (N*(N-1))
        return ic

    # Calculate the IC for each substring
    ics = [calculate_ic(substring) for substring in substrings]
    return ics

# Calculate the index of coincidences for m = 6, 7, 8
m_values = [6, 7, 8]
ics_results = {m: index_of_coincidence(cipher_text, m) for m in m_values}

#------------------PART 2--------------------------------------------------

# Splitting the cipher text into 7 substrings
substrings = ['' for _ in range(7)]
for i, char in enumerate(cipher_text):
    substrings[i % 7] += char

# Function to calculate the index of coincidence
def index_of_coincidence(text):
    N = len(text)
    freqs = Counter(text)
    ic = sum(freq * (freq - 1) for freq in freqs.values()) / (N * (N - 1))
    return ic

# Calculating the index of coincidence for each substring
ic_values = [index_of_coincidence(substring) for substring in substrings]








#----------------------------------------------------------------------------------------------------

# Function to add a custom title to the PDF pages
# This function is designed to modify its behavior for the first page
def add_custom_title_page(canvas, doc):
    canvas.saveState()  # Save the current state of the canvas to restore later
    canvas.setFont('Times-Bold', 16)  # Set font for the title
    # Draw the project title at the top of the page
    canvas.drawCentredString(letter[0]/2.0, letter[1]-108, "Project-2: Decrypting using Vigen`ere Cipher")
    if doc.page == 1:  # Check if it's the first page to include the prepared by line
        canvas.setFont('Times-Roman', 14)  # Set font for the authors
        # Draw the "Prepared by" line only on the first page
        canvas.drawCentredString(letter[0]/2.0, letter[1]-128, "Prepared by: Kinjal Pandey, Kritika Partha")
    canvas.restoreState()  # Restore the saved state

# Create a PDF document
# Heading for the section
content = [Paragraph(f"<b>Project-2: Decrypting using Vigen`ere Cipher</b>"), Spacer(1, 0.2 * inch)]
# Create a table with the algorithm steps
doc = SimpleDocTemplate("Vigenere_Cipher_Report.pdf",ppagesize=letter)

# Styles
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']

# Title
content.append(Paragraph("Index of Coincidence Analysis", styleH))
content.append(Spacer(1, 12))

# Introduction
intro_text = """This document provides the results of the Index of Coincidence (IC) analysis for the given cipher text with guessed keyword lengths of 6, 7, and 8. The IC values help in estimating the likelihood of a guessed keyword length being correct by comparing the structure of substrings with the expected distribution of letters in English."""
content.append(Paragraph(intro_text, styleN))
content.append(Spacer(1, 12))

# Analysis Results
analysis_results = "The Index of Coincidence (IC) values calculated for each substring with guessed keyword lengths are as follows: "
m6 = "- For m = 6, the IC values are approximately " + ", ".join(str(val) for val in ics_results[6])
m7 = "- For m = 7, the IC values are approximately " + ", ".join(str(val) for val in ics_results[7])
m8 = "- For m = 8, the IC values are approximately " + ", ".join(str(val) for val in ics_results[8])


explaination_ics= "An IC value close to 0.065 suggests that the substring is less random and more structured, resembling the distribution of a standard text in the corresponding language. This indicates that the substrings encrypted with the same key letter (if the guessed keyword length is correct) reveal a structure that resembles the natural frequency of letters in English."

content.append(Paragraph(analysis_results, styleN))
content.append(Spacer(1, 12))
content.append(Paragraph(m6, styleN))
content.append(Spacer(1, 12))
content.append(Paragraph(m7, styleN))
content.append(Spacer(1, 12))
content.append(Paragraph(m8, styleN))
content.append(Spacer(1, 12))
content.append(Paragraph(explaination_ics, styleN))
content.append(Spacer(1, 12))

# Conclusion
conclusion_text = """
Based on the calculated IC values, the analysis supports our guess that m = 7 is the correct keyword length for the ciphered text. This is because the IC values for m = 7 are the highest and most consistent, indicating a significant similarity to the expected distribution of letters in English text, and thus revealing a structure indicative of correct keyword length.
"""
content.append(Paragraph(conclusion_text, styleN))
content.append(Spacer(1, 0.2 * inch))


# Add a title
content.append(Paragraph("Index of Coincidence for Each Substring", styles["Title"]))
content.append(Spacer(1, 0.2 * inch))

# Add the substrings and their IC values to the report
for i, (substring, ic) in enumerate(zip(substrings, ic_values), start=1):
    content.append(Paragraph(f"Substring y{i}:", styles["Heading2"]))
    content.append(Paragraph(substring, styles["BodyText"]))
    content.append(Paragraph(f"Index of Coincidence: {ic:.4f}", styles["BodyText"]))
    content.append(Spacer(1, 0.2 * inch))

#--------------------------------------------------------------------------------------


# Given English letter frequencies
p = (0.082, 0.015, 0.018, 0.034, 0.104, 0.020, 0.016, 0.049, 0.063,
     0.003, 0.006, 0.035, 0.025, 0.067, 0.076, 0.020, 0.001, 0.055,
     0.061, 0.093, 0.028, 0.010, 0.023, 0.002, 0.020, 0.001)

# Function to calculate the frequency of each letter in a string
def calculate_frequencies(string):
    N = len(string)
    frequencies = {letter: 0 for letter in ascii_uppercase}
    for char in string.upper():
        if char in frequencies:
            frequencies[char] += 1
    return [frequencies[char]/N for char in ascii_uppercase]

# Function to cyclically shift a list
def cyclic_shift(lst, n):
    return lst[-n:] + lst[:-n]

# Compute dot product of two vectors
def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

y_values = substrings

# Initialize table data with headers
table_data = [["g Value"] + [f"Mg for y{idx+1}" for idx in range(len(y_values))]]

# Initialize a dictionary to store the Mg values for each y substring
mg_values = []

# Calculate Mg values for all possible shifts for each y value
for g in range(26):
    table_row = [g]
    for y in y_values:
        q = calculate_frequencies(y)
        vg = cyclic_shift(q, g)
        Mg = dot_product(p, vg)
        table_row.append(f"{Mg:.3f}")

        # Store the Mg value for this y in the dictionary
        mg_values.append(Mg)

    table_data.append(table_row)

# The table contains all Mg values for each g and y.


# Create the table
table = Table(table_data, colWidths=[1*inch] * (1 + len(y_values)))

# Add some style to the table
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
])
table.setStyle(style)

# Assuming content is a list that will be used to build the PDF document
content.append(table)
content.append(Spacer(1, 0.2 * inch))

# Build PDF
doc.build(content)

print(y_values)