# ~320 lines, somewhat less dense than avg -> ~250 lines = 3800 tokens ~= 15 tok/line
# Assuming openAI tokenizer, probably +/- 20%

def cost(lines: int) -> float:
    tok_cost_per_line = 15

    input_cost = 3/(10**6) # $3 per million tokens
    output_cost = 15/(10**6) # $15 per million tokens

    input_overhead = 0.5 # cons, actual guess: 0.2
    # total fraction of output tokens that must be supplied as prompt
    # this is a sum of multiple rounds of prompting and planning

    output_overhead = 1.0 # cons, actual guess: 0.3
    # fraction of output tokens that are duplicated (eventually erased or replaced)

    final_output_tok = lines * tok_cost_per_line
    input_tok = final_output_tok * (1 + input_overhead)
    output_tok = final_output_tok * (1 + output_overhead)
    print(input_tok, output_tok)
    return (input_tok * input_cost) + (output_tok * output_cost)

print(cost(250))