def parse_course_record (course_string):
  """
  Parses messy courses string into structured dict.

  param:
  - course_string (str) "code, name, credits, status"

  Returns: dict with 'code', 'name', 'credits' (int), 'status'
  """
  
  # Remove extra spaces and split the string at commas
  course_parts = course_string.strip().split(",")

  #Assign each part of the course string to a variable
  course_code = course_parts[0].strip().upper()
  course_name = course_parts[1].strip().lower()
  credits = int(course_parts[2].strip())
  status = course_parts[3].strip().lower()

  #Make the completion status consistent
  if status == "complete":
    status = "completed"

  # Create a dictionary with the course information
  course_record = {
    "code": course_code,
    "name": course_name,
    "credits": credits,
    "status": status
  }

  return course_record

def get_gen_ed_category (course_code, gen_ed_mapping):
  """
  Determines which Gen Ed category a course belongs to.

  Params:
  - Course_code (str): The course code being checked
  - gen_ed_mapping (dict): Dictionary containing course codes and their
  Gen Ed categories

  Returns: (str): The matching Gen Ed category or "uncategorized"
  """

  # Make sure the course code is uppercase
  course_code = course_code.strip().upper()

  # Check each category in the Gen Ed mapping
  for category, course_list in gen_ed_mapping.items():
    for code in course_list:
      if course_code == code.strip().upper():
        return category

  # Return Uncategorized if the course is not found
  return "Uncategorized"

def main ():

  # Given Data

  transcript = (  "    MTH-111, Pre-calculus, 4, COMPLETED    ",
    "  WR-121z, Composition I, 3, Completed   ",
    "  WR-122z,  Composition II, 3, Incomplete   ",
    "     GSWS-210, Violence Prevention, 4, completed",
  )

  gen_ed_categories = {
    "Creativity and Innovation": ["ART-133", "ART-291", 
                                  "ENG-105", "GSWS-210","MUS-330"],

    "Communication and Expression": ["ARTH-204", "ARTH-205",
                                     "BA-450", "BI-130",
                                     "MUS-311"],

    "Equity, Diversity, and Inclusion": ["ART-450", "ENG-214",
                                         "ES-220", "GSWS-312","MUS-205"],

    "Inquiry and Analysis": ["GSWS-300", "ES-200", "ENG-280", "BI-101",
                             "COMM-482"],

    "Numerical Literacy": ["CS-200", "MTH-111", "CS-346", "STAT-243z"
                           ],

    "Purposeful Learning": ["WR-121z","WR-122z", "WR-123"]

}

  # Step 1: Test parsing course records
  for course_string in transcript[:4]:
    print(parse_course_record(course_string))
  
  # Step 2: Test Gen Ed category lookup

  for course_string in transcript:
    course_record = parse_course_record(course_string)

    category = get_gen_ed_category(
        course_record["code"],
        gen_ed_categories
    )

    print(category)

if __name__ == "__main__":
  main()
