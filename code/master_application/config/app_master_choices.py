DATAMODE_CHOICES = (('A','Active'),('I', 'Inactive'),('D','Deleted'))
YES_NO_CHOICES = (('YES', 'Yes'), ('NO', 'No'))
APPROVED_UNAPPROVED_STATUS = (('UNAPPROVED', 'Unapproved'), ('APPROVED', 'Approved'), ('DENIED', 'Denied'))
DATA_LOADED_BY_CHOICES = (("SYSTEM", "System"),("USER", "User"))
DATA_WEEK_DAYS = [{"code":"MON", "name": "Monday"},
                  {"code":"TUE", "name": "Tuesday"},
                  {"code":"WED", "name": "Wednesday"},
                  {"code":"THU", "name": "Thursday"},
                  {"code":"FRI", "name": "Friday"},
                  {"code":"SAT", "name": "Saturday"},
                  {"code":"SUN", "name": "Sunday"}]
MODEL_DATA_WEEK_DAYS = (("MON", "Monday"),
                        ("TUE", "Tuesday"),
                        ("WED", "Wednesday"),
                        ("THU", "Thursday"),
                        ("FRI", "Friday"),
                        ("SAT", "Saturday"),
                        ("SUN", "Sunday"))
SUPER_USER_FIRSTNAME = "IT Support"
SUPER_USER_LASTNAME  = "IT Support"
SUPER_USER_NAME = "it-support"
SUPER_USER_EMAIL = "karthickvasu98@gmail.com"
SUPER_USER_PASSWORD = "secret123"
SUPER_USER_DATE_JOINED = 9080892903
SUPER_USER_LAST_LOGIN = 9080892903
SUPER_USER_IS_STAFF = True
SUPER_USER_IS_SUPERUSER = True
SUPER_USER_ACTIVE = True
SUPER_USER_EMAIL_VERIFIED = True
DEVICE_TYPE_CHOICES = (('PC','PC'),('LAPTOP','Laptop'),('MOBILE','Mobile'))
BUSINESS_LEGAL_IDENTIFICATION_NUMBER_TYPES = (("EIN", "Employer Identification Number"),("CIN", "Corporate Identification Number"))
BUSINESS_LEGAL_STRUCTURE_CHOICES = (("CCORP", "C-Corp"),("LLC", "LLC"))
SOCIAL_ACCOUNT_TYPE = (('GOOGLE','Google'),('FACEBOOK','Facebook'),('TWITTER','Twitter'),('LINKEDIN','LinkedIN'))
GENDER = (('MALE','Male'),('FEMALE','Female'),('OTHERS','Others'))
CURRENCY_CHOICES = (('INR (₹)', 'INR (₹)'), ('USD ($)', 'USD ($)'))
PROPERTY_DISPLAY_STATUS = (('DRAFT','Draft'),('PUBLISHED', 'Published'))
SERVICE_STATUS = (('DRAFT','Draft'),('PUBLISHED', 'Published'))
COMPANY_STATUS = (('DRAFT','Draft'),('PUBLISHED', 'Published'))
PROPERTY_EXCLUSIVITY = (("EXCLUSIVE", "Exclusive"), ("NON_EXCLUSIVE", "Non Exclusive"))
GEOGRAPHY_TYPE = (('STATE', 'State'), ('REGION', 'Region/Zone'), ('CITY', 'City'), ('CITY_AREA', 'City Area'))
MODE = (('PHYSICAL', 'Physical'), ('VIRTUAL', 'Virtual'))
VISIBILITY_CHOICES = (('N', 'No'), ('Y', 'Yes'))
SALUTATION_TYPE = (("mr", "Mr."), ("mrs", "Mrs."),("ms", "Ms."))
DAY = (("Monday","Monday"),("Tuesday","Tuesday"),("Wednesday","Wednesday"),("Thursday","Thursday"),("Friday","Friday"),("Saturday","Saturday"),("Sunday","Sunday"))
PAYMENT_TRANSACTION_STATUS = (('DUE', 'Due'), ('PAID', 'Paid'))
PROPERTY_STATUS = (('SOLD', 'Sold'), ('READY_TO_MOVE', 'Ready to move'), ('UNDER_CONSTRUCTION', 'Under Construction'))
PROPERTY_VERIFICATION_STATUS = (('VERIFIED', 'Verified'), ('VERIFICATION_FAILED', 'Verification Failed'), ('INPROCESS', 'Inprocess'))
APPROVAL_STATUS = (('WAITING_FOR_APPROVAL', 'Waiting for approval'), ('APPROVED', 'Approved'), ('DECLINED', 'Declined'))
ACCOUNT_USER_STATUS_CHOICES =  (("ACTIVE", "Active"),("INACTIVE", "Inactive"),("SUSPENDED", "Suspended"),("DELETED", "Deleted"),("INVITED", "Invited"))
IMAGE_REPO_FOLDER = 'dynamic_data/ir'
FILE_REPO_FOLDER = 'dynamic_data/fr'
ACCOUNT_CONTACT_LEVEL_CHOICES = (("PRIMARY", "Primary"),("SECONDARY","Secondary"))
DATA_TYPE_CHOICES = (('INTEGER', 'Integer'), ('TEXT', 'Text'), ('FLOAT', 'Float'), ('BOOLEAN', 'Boolean'))