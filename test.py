import warnings
from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("NumbersStation/nsql-350M")
model = AutoModelForCausalLM.from_pretrained("NumbersStation/nsql-350M")


# Suprime os avisos da biblioteca transformers
warnings.filterwarnings("ignore", message="Some weights of the model checkpoint at*")
warnings.filterwarnings("ignore", message="Setting `pad_token_id` to `eos_token_id`*")


text = """CREATE TABLE stadium (
    stadium_id number,
    location text,
    name text,
    capacity number,
    highest number,
    lowest number,
    average number
)

CREATE TABLE singer (
    singer_id number,
    name text,
    country text,
    song_name text,
    song_release_year text,
    age number,
    is_male others
)

CREATE TABLE concert (
    concert_id number,
    concert_name text,
    theme text,
    stadium_id text,
    year text
)

CREATE TABLE singer_in_concert (
    concert_id number,
    singer_id text
)

-- Using valid SQLite, answer the following questions for the tables provided above.

-- What is the maximum, the average, and the minimum capacity of stadiums ?

SELECT"""

inputs = tokenizer(text, return_tensors="pt")

# Agora você pode acessar input_ids e attention_mask como atributos de 'inputs'
generated_ids = model.generate(
    input_ids=inputs.input_ids,
    attention_mask=inputs.attention_mask, # AQUI ESTÁ A MUDANÇA CORRETA
    max_length=500
)
print(tokenizer.decode(generated_ids[0], skip_special_tokens=True))