"""Approximate request topics from keywords in request titles.

Used only to label points in the interactive nutshell. Titles never leave the
dataset: only the topic name is exported. The rules are first-match keyword
tagging, so they are approximate and are not part of any statistical test.
"""
import re

TOPICS = [
    ("Test request", r"\btest\s*-?\s*request"),
    ("Crime and policing", r"crime|police|\bpnp\b|cicl|\bcar\b|drug|oplan|\bgun|firearm|theft|robbery|murder|homicide"
                           r"|violence|\brape|carnap|arrest|jail|bjmp|\bpdl\b|inmate|prison|detain|trafficking|cyber"
                           r"|fraud|scam|illegal|violator|delinquen|juvenile|forensic|accident|incident|\bccj\b"),
    ("Health", r"health|dengue|covid|mortality|morbidity|patient|disease|vaccin|\bvax|hospital|\bckd\b|medical"
               r"|maternal|neonatal|nutrition|stunting|obesity|cancer|tubercul|\btb\b|hiv|mental|autism|cataract"
               r"|\bncmh\b|clinic|cases\b|death|philhealth|insurance claim"),
    ("Students and schools", r"enrol|student|faculty|academic|graduate|school|college|universit|scholar|teacher"
                             r"|curricul|admission|alumni|learner|tuition|\bbsed\b"),
    ("Land use and planning", r"\bclup\b|\bcdp\b|clwup|land use|land area|zoning|comprehensive (land|development)"
                              r"|development plan|\bmap|\bgis\b|hazard|subdivision|\blots?\b|cadastral|boundary"
                              r"|shapefile|\bcarp\b|barangay profile"),
    ("Water and utilities", r"water|consumer|sewer|sanitation|electric|energy|power|fuel|utilit|supply|connection"
                            r"|billing|tariff"),
    ("Environment and agriculture", r"climate|weather|rainfall|flood|river|tree|fish|forest|coast|marine|pamb|waste"
                                    r"|garbage|pollution|air quality|mangrove|wildlife|biodiversity|protected area"
                                    r"|mining|agricultur|farm|crop|rice|coconut|cacao|pest|livestock|animal|soil"
                                    r"|irrigation|disaster|typhoon|earthquake|drrm"),
    ("Housing, buildings and transport", r"road|bridge|transport|traffic|\bmrt|\blrt|rail|\bport\b|seaport|berth"
                                         r"|airport|terminal|building|housing|pabahay|settlement|redevelopment"
                                         r"|architect|geotechnical|construction|infrastructure|project|facilit"
                                         r"|vehicle|jeep|\bbus\b|ferry|ship|seafarer|aviation|flight|parking"),
    ("Budget, contracts and pay", r"budget|financ|procure|expenditure|salar|audit|revenue|\btax|income|fund|\bbid"
                                  r"|contract|payroll|allowance|cost|price|loan|borrower|bank|amlc|statement"),
    ("Population and jobs", r"population|census|household|resident|poverty|employee|workforce|wage|labou?r"
                            r"|employment|\bjobs?\b|\bofw|worker|personnel|plantilla|officials|beneficiar|4ps"
                            r"|senior citizen|\bpwd\b|solo parent|women|children|youth|generation z|lgbt"),
    ("Business and tourism", r"touris|establishment|business|permit|investment|trade|export|import|industry|msme"
                             r"|enterprise|hotel|resort|store|commercial|retailer|market|corporation|locator"
                             r"|buyer|concert|event"),
    ("Personal accounts and records", r"certificat|transcript|\btor\b|diploma|special order|birth|marriage"
                                      r"|records? of|my record|copy of|e-copy|clearance|national i\s?d|\bid\b"
                                      r"|license|verification|appointment|account|bp number|\bgsis|\bsss\b"
                                      r"|\bsim\b|lost|affidavit|signature|application"),
    ("Agency documents and policies", r"\birr\b|ordinance|polic|guideline|memorand|resolution|\bra\s?\d"
                                      r"|republic act|executive order|circular|manual|report|\bplan\b|program"
                                      r"|minutes|disposition schedule|charter|organi[sz]ational|rules of procedure"
                                      r"|constitution|by-?laws|\bbor\b|directory|statistic"),
]
GENERAL = "General data request"
_COMPILED = [(name, re.compile(pattern)) for name, pattern in TOPICS]


def topic(title):
    text = str(title).lower()
    for name, pattern in _COMPILED:
        if pattern.search(text):
            return name
    return GENERAL
