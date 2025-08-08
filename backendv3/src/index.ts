import dotenv from "dotenv";
dotenv.config();

import { query, type SDKMessage } from "@anthropic-ai/claude-code";
import { systemPrompt, testOutputClaude, userPrompt } from "./constants.js";
import { processWithStructuredOutput } from "./openai-processor.js";
import { createOliveIntegration } from "./olive-integration.js";

export const company_name = "Workweave"
const website_to_build = "https://www.vecflow.ai/"

async function main() {
    const messages: SDKMessage[] = [];
    let claudeOutput: any = null;

    try {
      // Step 1: Get output from Claude Code SDK with Neon MCP
      for await (const message of query({
        prompt: `${userPrompt({ website: website_to_build })}`,
        options: {
          appendSystemPrompt: systemPrompt,
          permissionMode: 'bypassPermissions',
          maxTurns: 100,
          mcpServers: {
            "neon": {
              "command": "npx",
              "args": [
                "-y",
                "@neondatabase/mcp-server-neon",
                "start",
                "napi_17j5cpiaia7ii4n95al28nlf44xchrtyzu5gpbseo43o0swksfsp373jv54uabnf"
              ]
            }
          }
        },
      })) {
        messages.push(message);
        console.dir(message, { depth: null });
        
        // Try to extract JSON from assistant messages
        if (message.type === 'assistant' && message.message?.content) {
          const content = typeof message.message.content === 'string' 
            ? message.message.content 
            : message.message.content.map((c: any) => c.type === 'text' ? c.text : '').join('');
          
          // Look for JSON in the message
          const jsonMatch = content.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            try {
              claudeOutput = JSON.parse(jsonMatch[0]);
              console.log("📊 Extracted Claude Output:", claudeOutput);
            } catch (e) {
              console.log("Failed to parse JSON from Claude response");
            }
          }
        }
      }

      // Step 2: Process with OpenAI structured output
      if (claudeOutput) {
        console.log("🤖 Processing with OpenAI structured output...");
        
        const structuredResult = await processWithStructuredOutput(
          claudeOutput
        );
        
        console.log("✅ Final Structured Output:");
        console.log(JSON.stringify(structuredResult, null, 2));
        
        return structuredResult;
      } else {
        console.log("Error processing with OpenAI structured output, returning Claude output only");
        return claudeOutput;
      }

    } catch (error) {
      console.error(`error building database for ${website_to_build}:`, error);
      throw error;
    }
}

// main();
(async () => {
  const structuredOutput = await processWithStructuredOutput(testOutputClaude);
  await createOliveIntegration(structuredOutput);
})();