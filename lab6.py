course_string = ( "    MTH-111, Pre-calculus, 4, COMPLETED    ",
    "  WR-121z, Composition I, 3, Completed   ",
    "  WR-122z,  Composition II, 3, Incomplete   ",
    "     GSWS-210, Violence Prevention, 4, completed"
  )

def parse_course_record (course_string):
  """
  Parses messy course string into structured dict.

  Param:
  - course_string (str) "code, name, credits, status"

  Returns: dict with 'code', 'name', 'credits' (int), 'status'
  """

  # Remove extra spaces and split the string at commas
  course_parts = course_string.strip().split(",")

  #Assign each part of the course string to a variable
  code = course_parts[0].strip().upper()
  name = course_parts[1].strip().lower()
  credits = int(course_parts[2].strip())
  status = course_parts[3].strip().lower()

  #Make the completion status consistent
  if status == "complete":
    status = "completed"

  # Create a dictionary with the course information
  course_record = {
    "code": code,
    "name": name,
    "credits": credits,
    "status": status
  }

  return course_record

def main ():
  #Test Task 1: parse_course_record()
  course1 = course_string[0]
  course2 = course_string[1]
  course3 = course_string[2]
  course4 = course_string[3]
  
  print(parse_course_record(course1))
  print(parse_course_record(course2))
  print(parse_course_record(course3))
  print(parse_course_record(course4))

if __name__ == "__main__":
  main()
  