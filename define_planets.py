# Define criteria of Planets

def isPlanet(average_hue,crater_count,average_lines):
            
   # In-Range-Function
   def inRange(value, lowerBound, upperBound):
         if value <= upperBound and value >= lowerBound:
            return True
         else:
            return False
 
# Define statistical Evaluation
   if inRange(average_lines, 1,50):
      if inRange(crater_count, 0,20):
         if inRange(average_hue, 100,120):
            return "Saturn"
      if inRange(crater_count, 30,150):
         if inRange(average_hue, 100,120):
            return "Mars"
      if inRange(crater_count, 150, 160):
         if inRange(average_hue, 105,115):
            return "Venus"
      if inRange(crater_count, 160,230):
         if inRange(average_hue, 0,105):
            return "Earth"

   if inRange(average_lines, 0,1):
      if inRange(crater_count, 18,40):
         if inRange(average_hue, 16,22):
            return "Neptune"
      if inRange(crater_count, 7,15):
         if inRange(average_hue, 18,23):
            return "Uranus"
      if inRange(crater_count, 0,20):
         if inRange(average_hue, 40,50) or inRange(average_hue, 10,14):
            return "Neptune"
         if inRange(average_hue, 90,96) or inRange(average_hue,33,39):
            return "Uranus"
         if inRange(average_hue, 100, 110):
            return "Jupiter"
      if inRange(crater_count, 20, 45):
         if inRange(average_hue, 35,45):
            return "Neptune"
         if inRange(average_hue, 113, 120):
            return "Mars"
         if inRange(average_hue, 100,109):
            return "Jupiter"
         if inRange(average_hue, 110,113):
            return "Mercury"
      if inRange(crater_count, 60,100):
         if inRange(average_hue, 112, 118):
            return "Mercury"
         if inRange(average_hue, 100,112):
            return "Jupiter"
      if inRange(crater_count, 101,120):
         if inRange(average_hue, 105,115):
            return "Mars"
      if inRange(average_hue, 105, 115):
         if inRange(crater_count, 121,160) or inRange(crater_count, 200,350):
            return "Venus"
      if inRange(crater_count, 350, 420):
         if inRange(average_hue, 45, 56):
            return "Earth"
      if inRange(crater_count, 420, 500):
         if inRange(average_hue, 100, 110):
            return "Mercury"
         