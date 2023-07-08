from CompassUTD.tools.google_search import (
    SearchCourse,
    SearchDegree,
    SearchDefinition,
    SearchGeneral,
)
from CompassUTD.tools.rate_my_professors import GetProfessorRMP
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

search_course = SearchCourse()
search_degree = SearchDegree()
search_general = SearchGeneral()
search_definition = SearchDefinition()
get_professor_rmp = GetProfessorRMP()
