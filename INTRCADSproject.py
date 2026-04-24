#importing needed libraries
import tkinter as tk
from tkinter import filedialog


#Function to load FASTA file
def load_fasta():
    file_path = filedialog.askopenfilename( filetypes=[("FASTA files", "*.fasta *.fa *.txt")])

    if not file_path:
        return


    dna = ""
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith(">"):
                dna += line.strip().upper()

    entry.delete(0, tk.END)
    entry.insert(0, dna)
    
#Insert new result and clear previous display
def show(text):
    output.delete("1.0", tk.END)
    output.insert(tk.END, text)
    
def analyze_dna():
    dna = entry.get().upper().replace(" ", "")

    if len(dna) == 0:
        show("Please enter or load a DNA sequence.")
        return
        
#validate dna        
    for n in dna:
        if n not in "ATGC":
             show("Invalid DNA sequence. \nSequences must contain A,T,G,C only.")
             return
        
#calculating DNA sequence length
    length=len(dna)

#Counting nucleotides
    counts = {'A':0,'T':0,'G':0,'C':0}
    for nucleotide in dna:
        counts[nucleotide] +=1

#calculating gc content
    gc_content = ((counts['G'] + counts['C'])/length)*100


    result = (
        f"DNA Length: {length}\n"
        f"A: {counts['A']}\n"
        f"T: {counts['T']}\n"
        f"G: {counts['G']}\n"
        f"C: {counts['C']}\n"
        f"GC Content: {gc_content:.2f}%"
     )

    show(result)
    
#Reverse complement of DNA
def reverse_complement():
    dna = entry.get().upper().replace(" ", "")

    if len(dna) == 0:
        show("Please enter or load a DNA sequence first.")
        return
    
    for n in dna:
        if n not in "ATGC":
            show("Invalid DNA sequence. \nSequences must contain A,T,G,C only.")
            return

    complement = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}

    rev_comp = ""
    for base in dna:
        rev_comp += complement[base]

    rev_comp = rev_comp[::-1]

    show(
        f"Reverse Complement:\n{rev_comp}\n\n"
        f"Length: {len(rev_comp)}"
    )

#Translation of DNA to protein
#Standard genetic code for translating DNA to protein
CODON_TABLE = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',  # Isoleucine and Methionine
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',  # Threonine
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',  # Asparagine, Lysine
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',  # Serine, Arginine
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',  # Leucine
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',  # Proline
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',  # Histidine, Glutamine
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',  # Arginine
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',  # Valine
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',  # Alanine
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',  # Aspartic acid, Glutamic acid
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',  # Glycine
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',  # Serine
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',  # Phenylalanine, Leucine
    'TAC':'Y', 'TAT':'Y',                        # Tyrosine
    'TGC':'C', 'TGT':'C',                        # Cysteine (C)
    'TGG':'W',                                   # Tryptophan
    'TAA':'_', 'TAG':'_', 'TGA':'_'              # Stop codons
}

# Function to translate a DNA sequence to a protein string
def translate_protein():
    dna = entry.get().upper().replace(" ", "")
    
    if len(dna) <= 2:
        show("DNA sequence should be at least 3 neucleotides for protein translation.")
        return

    for n in dna:
        if n not in "ATGC":
            show("Invalid DNA sequence. \nSequences must contain A,T,G,C only.")
            return
    
    protein = ""
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i:i+3]
        if codon in CODON_TABLE:
            amino_acid = CODON_TABLE[codon]
            if amino_acid == '_':  # Stop codon found
                break
            protein+=amino_acid

    show(
         f"Protein Sequence:\n{protein}\n\n"
         f"Protein Length: {len(protein)}"
    )


#Clear input and output
def clear_button():
    entry.delete(0,tk.END)
    output.delete("1.0",tk.END)
    
#Creating a GUI interface

window = tk.Tk()
window.title("DNA Sequence Analysis Tool")

tk.Label(window, text="DNA Sequence:").pack()
entry = tk.Entry(window, width=60)
entry.pack()

tk.Button(window, text="Load FASTA File", command=load_fasta).pack()
tk.Button(window, text="Analyze Sequence", command=analyze_dna).pack()
tk.Button(window, text="Reverse Complement", command=reverse_complement).pack()
tk.Button(window, text="Translate Protein", command=translate_protein).pack()
tk.Button(window, text="Clear All", command=clear_button).pack()

output = tk.Text(window, height=12, width=60)
output.pack()

window.mainloop()
