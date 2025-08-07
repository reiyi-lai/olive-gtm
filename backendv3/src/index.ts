import { query, type SDKMessage } from "@anthropic-ai/claude-code";
import { systemPrompt, userPrompt } from "./constants.js";
import { processWithStructuredOutput } from "./openai-processor.js";

const website_to_build = "workweave.dev"

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
      }

      // Step 2: Process with OpenAI structured output (if custom prompt is provided)
      if (claudeOutput && process.env.CUSTOM_PROMPT) {
        console.log("🤖 Processing with OpenAI structured output...");
        
        const structuredResult = await processWithStructuredOutput(
          claudeOutput
        );
        
        console.log("✅ Final Structured Output:");
        console.log(JSON.stringify(structuredResult, null, 2));
        
        return structuredResult;
      } else {
        console.log("ℹ️ No custom prompt provided, returning Claude output only");
        return claudeOutput;
      }

    } catch (error) {
      console.error(`error building database for ${website_to_build}:`, error);
      throw error;
    }
}

main();