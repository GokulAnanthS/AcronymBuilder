"""
Object: acronymBuilder
Discription: Generates accronym based on specific conditions
Input: files contains abbriviation
Output: files contain acronym
"""
class AcronymBuilder:

    # predefined attributes
    def __init__(self):
        self.letter_scores = {}
        self.remaining = {}
        self.indexedNames = []
        self.names=[]
        self.valuesFile = 'values.txt'

    # Reads a list of abbriviation from the given file
    def readFile(self, file_name):
        try:
            with open(file_name, 'r') as file:
                self.names = [line.rstrip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
            return []
        
    # Writes the result of acronym generated.
    def writeToFile(self, file_name):
        sorted_items = sorted(self.remaining.items(), key=lambda x: x[1][1])
        try:
            with open(file_name, 'w') as file:
                for i in self.names:
                    for j in sorted_items:                        
                        if i == j[1][0]:
                            print(i,j[0],j[1][1])
                            file.write(f"{i}\n{j[0]}\n")
                            break
            # print(f"Results written to '{file_name}' successfully.")
        except Exception as e:
            print(f"Error writing to file '{file_name}': {e}")

    # Read values for calculating score.
    def readValues(self):
        try:
            with open(self.valuesFile, 'r') as f:
                letter_values = [line.rstrip().split(' ') for line in f.readlines()]
                for score in letter_values:
                    self.letter_scores[score[0].upper()] = int(score[2]) if score[1] == '' else int(score[1])
        except Exception as e:
            print(f"Error writing to file '{self.valuesFile}': {e}")

    # Transform the abbriviation into simple for calculation
    def splitName(self,name):
        words = []
        word = ''
        for i in range(len(name)):
            if name[i]=="'":
                i+=1
            elif name[i].isalpha():
                word += name[i]
            else:
                if word:
                    words.append(word.upper())
                word = ''
        if word:
            words.append(word.upper())
            return words
        
    # append indexes for every word into a single list
    def generateIndex(self, words):
        self.indexedNames=[]
        for word in words:
            for i in range(len(word)):
                self.indexedNames.append([word[i], i])

    # calculate score for each character
    def calculateScore(self,index,indexedNames):
        if(indexedNames[index][1]==0):
            return 0
        elif index == len(indexedNames) - 1 or (index + 1 < len(indexedNames) and indexedNames[index+1][1] == 0):
            if indexedNames[index][0] == "E":
                return 20
            else:
                return 5
        else:
            return indexedNames[index][1]+ self.letter_scores[indexedNames[index][0]]
        
    # Pre-processing and Post-processing
    def abbriviations(self):
        self.readValues()
        for name in self.names:
            words = self.splitName(name)
            self.generateIndex(words)
            self.generateAcronym(name)
        self.remaining = {key: value for key, value in self.remaining.items() if value[2] <= 1}

    # Generates Acronym for given name
    def generateAcronym(self, name):
        for i in range(1, len(self.indexedNames) - 1):
            second_letter_total = 0
            third_letter_total = 0
            for j in range(i + 1, len(self.indexedNames)):
                abbreviation = self.indexedNames[0][0] + self.indexedNames[i][0] + self.indexedNames[j][0]
                second_letter_total = self.calculateScore(i, self.indexedNames)
                third_letter_total = self.calculateScore(j, self.indexedNames)

                if abbreviation not in self.remaining:
                    self.remaining[abbreviation] = [name, second_letter_total + third_letter_total, 1]
                elif (
                    self.remaining[abbreviation][1] >= second_letter_total + third_letter_total
                    and self.remaining[abbreviation][0] == name
                ):
                    self.remaining[abbreviation][1] = second_letter_total + third_letter_total
                    self.remaining[abbreviation][2] += 1
                elif (
                    self.remaining[abbreviation][1] != second_letter_total + third_letter_total
                    and self.remaining[abbreviation][0] != name
                ):
                    self.remaining[abbreviation][2] += 1  

def main():
    generator = AcronymBuilder()
    generator.readFile('names.txt')
    generator.abbriviations()
    generator.writeToFile('sasi_kumar_tree_abbrevs.txt')

if __name__ == "__main__":
    main()