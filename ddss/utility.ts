import * as readline from "node:readline";

export function strRuleGetStrIdea(data: string): string | null {
    if (!data.startsWith("--")) {
        const lines = data.split("\n");
        if (lines.length > 0) {
            return `----\n${lines[0]}\n`;
        }
    }
    return null;
}

/**
 * Patches process.stdout.write to prevent asynchronous logs from messing up the readline prompt.
 */
export function patchStdout(rl: any) {
    const originalWrite = process.stdout.write;
    let isReprompting = false;

    // @ts-ignore
    process.stdout.write = (chunk: string | Uint8Array, encoding?: any, callback?: any) => {
        if (isReprompting) {
            return originalWrite.call(process.stdout, chunk, encoding, callback);
        }

        const str = chunk.toString();

        // If it's just a newline (like when the user hits Enter), let it pass through.
        // This allows the input line to stay in the terminal history.
        if (str === "\n" || str === "\r\n") {
            return originalWrite.call(process.stdout, chunk, encoding, callback);
        }

        if (str.includes("\n")) {
            // Move to start of line and clear it (wiping the current prompt display)
            originalWrite.call(process.stdout, "\r\x1b[K");

            const result = originalWrite.call(process.stdout, chunk, encoding, callback);

            isReprompting = true;
            // Redraw the prompt and current input buffer on the NEW line
            rl.prompt(true);
            isReprompting = false;

            return result;
        }

        return originalWrite.call(process.stdout, chunk, encoding, callback);
    };

    return () => {
        // @ts-ignore
        process.stdout.write = originalWrite;
    };
}
