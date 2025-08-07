import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, // Make sure to set this in your environment
});

interface ToolSuggestion {
  title: string;
  prompt: string;
  features: string[];
}

interface StructuredOutput {
  tool_suggestions: ToolSuggestion[];
  connection_string: string;
}

// ClaudeOutput is now just the raw output from Claude Code SDK
type ClaudeOutput = any;

export async function processWithStructuredOutput(
  claudeOutput: ClaudeOutput,
  customPrompt: string,
  count: number = 5
): Promise<StructuredOutput> {
  const response = await client.beta.chat.completions.parse({
    model: "gpt-4o-2024-08-06",
    messages: [
      {
        role: "system",
        content: `You are a tool for Olive, an app which lets companies plug in their database, and generate internal tools using prompts through LLMs. Olive's goal is to let companies build internal tools quickly and easily, and allow for the possibility of having many different types of insight into their product(s).

Your job is to generate some example prompts for the user, which they could then use in order to pass to the LLM to generate an internal tool, based on the database schema and the database itself as follows:

Each tool should:
    - Solve a real operational or coordination problem
    - Be implementable with SQL queries and CRUD APIs
    - Be useful to roles like founders, ops, product, eng, support, or sales
    - Assume the frontend is a web-based app using standard inputs/tables
    - Be intended for employees of the business (founders, engineers, marketers, etc.)

You must NOT suggest:
    - Anything that relies on external APIs or realtime infra
    - AI-generated summaries, predictions, or magic
    - New database tables or schema changes
    - anything that is meant for customers of the company's product, as this is purely for employees of the business (founders, engineers, marketers, etc.) This includes if the tool is meant for an enterprise application, where their customers might be founders, engineers, etc.

The tools can be dashboards, workflows, review queues, editors, explorers, or triage interfaces — anything that helps users **see what matters and act fast**

Each idea must be distinct — no overlap or redundant views. they should vary in target user and business purpose.

If a feature or insight cannot be *explicitly constructed from SQL-accessible data already in the schema*, do not include it.

The suggestions that are generated should be one of the following:
    - Insight focused (e.g. "View the most active contacts in your network")
    - Customer management focused (e.g. "Manage permissions for customers")
    - Something else that is business focused

CRITICAL: these are tools for the company who owns the database. they are not for the end users of the database or their product. this is critical to know for suggesting the correct tools. Do NOT suggest tools that are for the customers of the company's product.

Output a list of ${count} ideas. Each should have:
    - title (max 8-10 words, specific and useful)
    - prompt: a 2-3 sentence description of what this tool lets a team do and why it's valuable
    - features: 4-5 real, UI-level actions or components it would contain

Claude's Raw Output (Database and Company Information):
${JSON.stringify(claudeOutput, null, 2)}`
      },
      {
        role: "user", 
        content: customPrompt
      }
    ],
    response_format: {
      type: "json_schema",
      json_schema: {
        name: "tool_suggestions_response",
        strict: true,
        schema: {
          type: "object",
          properties: {
            tool_suggestions: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  title: { type: "string" },
                  prompt: { type: "string" },
                  features: {
                    type: "array",
                    items: { type: "string" }
                  }
                },
                required: ["title", "prompt", "features"],
                additionalProperties: false
              }
            },
            connection_string: { type: "string" }
          },
          required: ["tool_suggestions", "connection_string"],
          additionalProperties: false
        }
      }
    }
  });

  return response.choices[0].message.parsed as StructuredOutput;
}

// Example usage function
export async function processClaudeOutputExample(claudeOutput: ClaudeOutput, count: number = 2) {
  const examplePrompt = `Generate ${count} internal tool suggestions based on the database schema and company information. Also extract the connection string from the Claude output.`;
  
  try {
    const structured = await processWithStructuredOutput(claudeOutput, examplePrompt, count);
    console.log("Structured Output:", structured);
    return structured;
  } catch (error) {
    console.error("Error processing with OpenAI:", error);
    throw error;
  }
}