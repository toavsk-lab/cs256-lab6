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

def audit_credits(student_bins):
  """
  Calculates the total completed credits for each Gen Ed category

  Params:
  - student_bins (dict): A dictionary containing Gen Ed categories
  and lists of course codes and credits

  Returns (dict): A dictionary containing the total credits for each category
  """

  # Create a credit total of zero for each category
  credit_totals = {}

  # Initialize credit totals for each category
  for category in student_bins:
    credit_totals[category] = 0

  # Calculate the total credits for each category
  for category, course_list in student_bins.items():
    for course_code, credits in course_list:
      credit_totals[category] += credits

  return credit_totals

def bin_student_courses(transcript, gen_ed_mapping):
  """
  Groups completed courses into their Gen Ed categoris

  params:
  - transcript (tuple): A collection of string containing course records
  - gen_ed_mapping (dict): A dictionary mapping course codes to categories

  Returns (dict): Categoris containing lists of course codes and credits
  """

  student_bins = {}

  # Create an empty list for each Gen Ed category
  for category in gen_ed_mapping:
    student_bins[category] = []

  # Create an empty list for uncategorized courses
  uncategorized = get_gen_ed_category ("", gen_ed_mapping)
  student_bins[uncategorized] = []

  # Process each course in the transcript
  for course_string in transcript:
    course_record = parse_course_record(course_string)

    course_code = course_record["code"]
    credits = course_record["credits"]
    status = course_record["status"]

    # Find the course's Gen Ed category
    category = get_gen_ed_category(
        course_code,
        gen_ed_mapping
      )

    # Add the course code and credits to its category
    student_bins[category].append(
        (course_code, credits)
    )

  return student_bins


def main ():

  # Given Data

  transcript = (  "    MTH-111, Pre-calculus, 4, COMPLETED    ",
    "  WR-121z, Composition I, 3, Completed   ",
    "  WR-122z,  Composition II, 3, Incomplete   ",
    "     GSWS-210, Violence Prevention, 4, completed",
    "   EMDA-250, Introduction to arts based research, 3, complete   ",
    "   ENG-214, Language Diversity in the USA, 4, Incomplete  ",
    "   ART-133, Introduction to drawing, 4, Incomplete   ",
    "   ARTH-204, History of Art: Prehistory Through Medieval, 4, incomplete  ",
    " COMM-349, Political Communication, 4, Complete    ",
    "  ENG-414, Writing for Publication, 4, Complete    ",
    "    PSY-475, Crisis Intervention Strategies, 4, Complete   ",
    " TA-169, Elements of Design, 3, Incomplete         ",
    "ES-220, Environmental Justice, 4, Complete     ",
    "              HIST-348, Marx and Jesus in Latin America, 4, Incomplete",
    "   PSY-472, Sustainable Compassion, 3, Incomplete",
    "  EC-202, Principles of Macroeconomics, 4, Complete",
    "     HST-250, American Life and Culture, 4, Incomplete",
    "   STAT-243Z, Introduction to Statistical Methods, 4, Incomplete        "
  )

  gen_ed_categories = {
    "Creativity and Innovation": ["ART-133", "ART-291", "ARTH-330", "BI-140",
                                  "CCJ-361", "COMM-486", "COMM-222",
                                  "COMM-424", "CS-210", "DCIN-331", "ED-456",
                                  "ED-474", "EMDA-355", "ENG-105", "ENG-315",
                                  "ES-327", "GSWS-210", "GSWS-313", "GSWS-410",
                                  "MUS-202", "MUS-210", "MUS-330"],

    "Communication and Expression": ["ARTH-204", "ARTH-205", "ARTH-206",
                                     "BA-450", "BA-490", "BA-324", "BI-130",
                                     "CCJ-385", "COMM-214", "COMM-203",
                                     "COMM-330", "COMM-349", "COMM-353",
                                     "CS-310", "ED-398", "ED-240", "ED-252",
                                     "ED-437", "GSWS-321", "GSWS-221",
                                     "GSWS-311", "SPAN-310", "MUS-311"],

    "Equity, Diversity, and Inclusion": ["ART-450", "ENG-214", "ENG-245",
                                         "ENG-447B", "ENG-447E", "ERS-201",
                                         "FL-205", "GSWS-222", "GSWS-310",
                                         "HST-339", "HST-349", "SOAN-213",
                                         "SOAN-323", "TA-348", "TA-349",
                                         "ES-220", "GSWS-312","MUS-205"],

    "Inquiry and Analysis": ["GSWS-300", "ES-200", "ENG-280", "BI-101",
                             "COMM-482", "BA-411", "BA-483", "CCJ-230",
                             "CCJ-424", "COMM-303", "COMM-343", "EC-202",
                             "EC-325", "ED-473", "ED-438", "EMDA-250", "ES-130",
                             "ES-200", "PHL-201", "SOAN-204", "SOAN-211",
                             "HE-453"],

    "Numerical Literacy": ["CS-200", "MTH-111", "CS-346", "STAT-243z",
                           "BA-218", "BA-420", "CS-346", "MTH-111Z", "MTH-212",
                           "MTH-361", "SOAN-329", "STAT-243Z"],

    "Purposeful Learning": ["WR-121z","WR-122z", "WR-123"]
}

  # # Step 1: Test parsing course records
  # for course_string in transcript[:4]:
  #   print(parse_course_record(course_string))
  
  # # Step 2: Test Gen Ed category lookup

  # for course_string in transcript:
  #   course_record = parse_course_record(course_string)

  #   category = get_gen_ed_category(
  #       course_record["code"],
  #       gen_ed_categories
  #   )

  #   print(category)

  # # Step 3: Audit completed credits
  # student_bins = bin_student_courses(
  #     transcript,
  #     gen_ed_categories
  # )

  # # Step 4: Bin completed courses
  # student_bins = bin_student_courses(
  #     transcript,
  #     gen_ed_categories
  # )

  # for category, courses in student_bins.items():
  #   print(f"{category}: {courses}")

  # Run the final pipeline to organize completed course
  student_final_bins = bin_student_courses(
      transcript,
      gen_ed_categories
  )

  # Display the completed courses in each category
  for category, courses in student_final_bins.items():
    print(f"{category}: {courses}")

  # Calculate the completed credits in each category
  credit_totals = audit_credits(student_final_bins)

  # Display the credit totals
  for category, credits in credit_totals.items():
    print(f"{category}: {credits} credits")

if __name__ == "__main__":
  main()
