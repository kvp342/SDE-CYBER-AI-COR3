# Prompt injection

## Direct injection
Direct prompt injection is when the user's own message tries to make the model drop its rules, expose its hidden setup or produce forbidden output.

## Indirect injection
Indirect prompt injection hides instructions inside content the model reads, such as a web page, an email or a retrieved document. The model may treat that data as a command.

## Defences
Keep instructions and data separate with clear delimiters, tell the model that document text is data, filter retrieved text for instruction-like lines, and check outputs for leaked secrets or unknown links. No single defence is complete, so combine layers and measure attack success rate.

## Canary tokens
A canary token is a random string placed in the system prompt. If it ever appears in an answer, the hidden instructions have leaked.
