import OpenAI from "openai";
import { z } from "zod";


const StructuredOutput = z.object({
  tool_suggestions: z.array(z.object({
    title: z.string(),
    prompt: z.string(),
    features: z.array(z.string()),
  })),
  connection_string: z.string(),
});

type ClaudeOutput = any;

export async function processWithStructuredOutput(
  claudeOutput: ClaudeOutput,
  count: number = 2
): Promise<z.infer<typeof StructuredOutput>> {
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  });

  const jsonSchema = {
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
  };
  
  console.log('jsonSchema', jsonSchema);

  const response = await openai.responses.parse({
    model: "gpt-4o-2024-08-06",
    input: [
      {
        role: "user",
        content: `You are a tool for Olive, an app which lets companies plug in their database, and generate internal tools using prompts through LLMs. Olive's goal is to let companies build internal tools quickly and easily, and allow for the possibility of having many different types of insight into their product(s).

Your job is to generate some prompts to pass to the LLM to generate an internal tool each, based on the company information and database context as shown below:
${JSON.stringify(claudeOutput, null, 2)}

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
    - features: 4-5 real, UI-level actions or components it would contain`
      }
    ],
    text: {
      format: {
        type: 'json_schema',
        name: 'output',
        schema: jsonSchema,
      },
    }
  });

  console.log('output_parsed', response.output_parsed);

  return response.output_parsed!;
}