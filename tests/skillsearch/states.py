from alexafsm.states import with_transitions, States as StatesBase
from alexafsm import response
from alexafsm import amazon_intent

from tests.skillsearch.skill import Skill
from tests.skillsearch.intent import NTH_SKILL, PREVIOUS_SKILL, NEXT_SKILL, NEW_SEARCH, \
    DESCRIBE_RATINGS, LAUNCH_SURVEY, WIFI_PASSWORD
from tests.skillsearch.session_attributes import SessionAttributes, ENGLISH_NUMBERS

MAX_SKILLS = 6
SKILL_NAME = "Skill Search"
DEFAULT_PROMPT = "What skill would you like to find?"
HELP = f"{SKILL_NAME} helps you search for skills. You can ask questions such as:" \
       f" how do i order pizza, or, I want to meditate." \
       f" For each question, {SKILL_NAME} only retrieves the most relevant skills." \
       f" In order to use a skill you find, you must first exit {SKILL_NAME} and then tell Alexa" \
       f" to open that skill." \
       f" {DEFAULT_PROMPT}"
HEAR_MORE = "Would you like to hear more about it?"
IS_THAT_ALL = "Will that be all?"


def _you_asked_for(query: str):
    return f"You asked for {query}. "


def _get_verbal_skill(skill: Skill) -> str:
    """Get the natural language representation of a skill """
    return skill.name


def _get_verbal_ratings(skill: Skill, say_no_reviews: bool = True) -> str:
    """Get a verbal description of the rating for a skill
    say_no_reviews: if there are no reviews, this will mention that explicitly
    """
    if skill.num_ratings > 0:
        return f"has an average rating of {skill.avg_rating} from {skill.num_ratings} reviews"
    if say_no_reviews:  # there are no reviews, and we want to tell the user that explicitly
        return "has no reviews at this time"
    return ""  # there are no reviews, but we don't need to tell the user that


def _get_highlights(skill: Skill):
    """Get highlights for a skill"""
    if 'highlight' in skill.meta:
        return '\n'.join([h for _, hs in skill.meta.highlight.to_dict().items() for h in hs])

    return skill.description



class States(StatesBase):
    """
    A collection of static methods that generate responses based on the current session attributes.
    Each method corresponds to a state of the FSM.
    """

    session_attributes_cls = SessionAttributes
    skill_name = SKILL_NAME
    default_prompt = DEFAULT_PROMPT
    # states to exit on when user requests Alexa to stop talking
    EXIT_ON_STOP_STATES = ['no_result', 'search_prompt', 'is_that_all', 'bad_navigate',
                           'no_query_search']
    # states to continue on when user requests Alexa to stop talking
    CONTINUE_ON_STOP_STATES = ['describing', 'has_result', 'describe_ratings']
    # states to prompt user for new search when user requests Alexa to stop talking
    PROMPT_ON_STOP_STATES = ['initial', 'helping']
    # initial is its own special thing -- don't exit when interrupting the initial help message

    def initial(self) -> response.Response:
        welcome_speech = f"Welcome to {self.skill_name}. {HELP}"

        return response.Response(
            speech=welcome_speech,
            reprompt=self.default_prompt
        )

    @with_transitions(
        {'trigger': amazon_intent.HELP,
         'source': '*',
         'auto_transition': 'test_state'}
    )
    def helping(self) -> response.Response:
        return response.Response(
            speech=HELP,
            reprompt=DEFAULT_PROMPT
        )

    @with_transitions(
    )
    def test_state(self) -> response.Response:
        return response.Response(
            speech="the auto transition worked",
            reprompt=DEFAULT_PROMPT
        )

    @with_transitions(
        {'trigger': WIFI_PASSWORD,
         'source': '*',
         }
    )
    def password_response(self) -> response.Response:
        return response.Response(
            speech="The password is X Y Z",
            reprompt="sgdsgsd"
        )

    @with_transitions(
        {'trigger': LAUNCH_SURVEY,
         'source': '*',
         'prepare': 'fetch_survey_list',
         'conditions': 'valid_survey_name'}
    )
    def process_survey(self) -> response.Response:
        return response.Response(
            speech="sdsdsf",
            reprompt="sgdsgsd"
        )

    #@with_transitions(
    #     {
    #         'trigger':
    #     }
    # )

    @with_transitions(
        {'trigger': amazon_intent.HELP,
         'source': '*'}
    )
    def helping(self) -> response.Response:
        return response.Response(
            speech=HELP,
            reprompt=DEFAULT_PROMPT
        )


    @with_transitions(
        {
            'trigger': amazon_intent.NO,
            'source': 'describe_ratings'
        },
        {
            'trigger': amazon_intent.CANCEL,
            'source': CONTINUE_ON_STOP_STATES
        },
        {
            'trigger': amazon_intent.STOP,
            'source': CONTINUE_ON_STOP_STATES
        }
    )
    def is_that_all(self) -> response.Response:
        """when we want to see if the user is done with the skill"""
        return response.Response(
            speech=f"Okay, {IS_THAT_ALL}",
            reprompt=IS_THAT_ALL
        )

    @with_transitions(
        {
            'trigger': amazon_intent.YES,
            'source': ['describing', 'is_that_all']
        },
        {
            'trigger': amazon_intent.CANCEL,
            'source': EXIT_ON_STOP_STATES
        },
        {
            'trigger': amazon_intent.STOP,
            'source': EXIT_ON_STOP_STATES
        },
    )
    def exiting(self) -> response.Response:
        return response.end(SKILL_NAME)
