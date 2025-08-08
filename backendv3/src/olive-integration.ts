export async function createOliveIntegration(structuredOutput: any) {
  const { tool_suggestions, connection_string } = structuredOutput;

  console.log("🫒 Starting Olive integration...");

  // Step 1: Create database connection
  console.log("Creating database connection...");
  const dbResponse = await fetch('http://dev.fromolive.com:3001/trpc/database.create?batch=1', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Cookie': 'wos-session=Fe26.2*1*1276cf49dec579ff502c5b22552afc3b296963b07589674b6a862bba2cc7209e*DcQzwywbX8ifX00Fj_a8Xg*bKRGosBP66YuYCjljrgriGapy1nmx5-J9mFHgr-thwYpxWQL1XAvidPfZ2JAidUTtcXvmHfHdMuvQxC5a4CcHH9quTMbJ8bhMXgxfcEj8VX2xHE-_eJsABOi_Oe4nBAtGb27B_WiJjZdl7dC-cwpr9Oq6u390Q0wWpDMDojbM6pQ79dq64x2LdYFcgnGPz_EfqNHmnb-zceHKzMUNRx4R312DNbaKOMG5n6pcteZlu_KE3hSPmYuN1V1hWA8vgkMbzY3TaIriT0PN6Q1E48mdXy4J4_v-jzUzTX6fn-hHB2CKOvG9vtQhfPF4x4JM7hl0MKi_k-LbJT36cKu-ViZ78ZLv1Y8gKYpHCz1ywImw2WrsJklZP3bwuEQuHmaUNpBQA0x91fT5_f1ayr3TJrSizRCJ_WeIGpCV7lGwXlVFDVC_SM64uPQgER0wWhsIqDMz_xU_oEXqDNjGNUj_7VkRd7bKtImXelzo-2y-vsfgnMwtgP3Xxgl96j1tFs2jgoZemtOHJGE410i6l8ov5ZH3Ibz6-rwHB6D-TD2M6atnYSVMkfF7_mzmdeIgfHkDkCRbEIgbW0HIMMp--ohpWUmlCIMrEkiSsusRGEtrJJrGm6y8TezOkEHM5TwYUmU5LS8Sp2IFHpMt5dQVswyJADTj6nggE4RDUbc0G09SGCIoFW-bLW4Jv1SPwL7jM4uNyIt71MulD8P33-H8W9MoIrNKqqq7AZ3WzgvCmHxVezzK0dqBfTeCHV0wCu2v12FV_a3ZEUY6AmNnthpW6Yj7_b7SSN4E_iK1Q8sJtiO4-0crl7l5sOjFUgMdkcyAMJhn39csFV0hfUmEtcCRLHW9HkGx61ti91f6v3Tx96N7nWFeBj_Rigo93vEuNHXpzxNukIEXHKPOrp-hc1YjaqJgfGngpgu0gRWq5dn5LRaUMgIIDmduJtIjjlA1OzjveMPS_scLFLssVRQsnuXQDJIVWEArc38yBuuxpYNuWf2o-gWhE9JwdfSWi00h7TD-mm1UirpFA3cgpQP9MvJOSmqJfyu5WZTZJMObllHmLkHtFStEdY0jYpjkeA-fAm1Qaaa1ONKIjpQavvlsFVWJ21n-AyEs7cBTRqcU2FrF-rKWgPdoR9AMCyDlvSv6fme0oBMQ-MxmDqXgZP4nt_PT2oDXezK4KcI0iyojLYsFuNd0rP-sDZlTcY0u66C8apjiSNAb1xwb9w-Cj4Jk2OXtZ_ygzX7EYzzH_nogbVNeIoVvBwBx1E27RbvAg2WIUqpnE1i3lWneoe0ig93cAqW5IOCs8SN5iHSO4m5eCq02TEbGjoif3kg5-6JEd71Bv3pRbtF8zah2uFYu8fR-awcca6wJgajq9iSa_jaN4l1RraSYQ2mBEeRc4gxk-0ddWdAYgwSkI-Y8kow18B9yGSdlkJad1mOZ1AvKfo0ow18RHTwAjLoKoEyhjpHVueQ0yH9jZtUyG0tFBu0vhmDkh_ZlkxlaXiwF2QiqUzHiEna9fval6YM1BFiE4h0Yy_O2Gk5g-ksrPeR80UgERdxYkUE_0DCQtIncMV7BK4fTjdW5yHAHTF9zxPISk4KBZ4jl7tG12DJIg9MB5ctNiMIZAmK__8sZIPe2AQF4suoyAFh0Ri1atDmIEY21xwp68hKrRsDe7Erb_n_n1Z-__jh06kti_objuE2luiMrZ8R5um6mfNL4Xh7i1dMqDTVl1nnhIi0CfnK4YEmDKjp3kF0pbV9KNEWsrsAMUFoX9IkEBRjMXizm3GkSvsWIS3ik4VRaUJmkikXRrwzYCJOCzdPwM-qBsxNDHnBvaEic4J-thCMu1db4tFuwziyoj678AdO5xIZYk0IK-hBgku5mswX5cF7CpyrA6vQ-Q**eb2201454b8bd2dcb4c314e6565e0151068e75e60fac2cc0c3e833533a11f584*BgpZmzf2qYyZeXmvqZj1RegjsxQhFCxft-64P5heNoA~2; olive-auth=1754609124460'
    },
    body: JSON.stringify({
      "0": {
        json: {
          name: `${tool_suggestions[0]?.title} Database`,
          connectionString: connection_string,
          sslMode: "require"
        }
      }
    })
  });

  if (!dbResponse.ok) {
    const errorText = await dbResponse.text();
    console.error("🔍 Database creation error response:", errorText);
    throw new Error(`Database creation failed: ${dbResponse.status} ${dbResponse.statusText} - ${errorText}`);
  }

  const database = await dbResponse.json();
  console.log("🔍 Database response:", JSON.stringify(database, null, 2));
  
  // tRPC batch response is an array, get first item, then navigate to the ID
  const dbId = database[0].result.data.json.id;
  console.log(`✅ Database created with ID: ${dbId}`);

  // Step 2: Create apps for each tool suggestion
  for (let i = 0; i < tool_suggestions.length; i++) {
    const tool = tool_suggestions[i];
    console.log(`Creating app ${i + 1}/${tool_suggestions.length}: ${tool.title}`);

    const appResponse = await fetch('http://dev.fromolive.com:3001/trpc/app.create?batch=1', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cookie': 'wos-session=Fe26.2*1*1276cf49dec579ff502c5b22552afc3b296963b07589674b6a862bba2cc7209e*DcQzwywbX8ifX00Fj_a8Xg*bKRGosBP66YuYCjljrgriGapy1nmx5-J9mFHgr-thwYpxWQL1XAvidPfZ2JAidUTtcXvmHfHdMuvQxC5a4CcHH9quTMbJ8bhMXgxfcEj8VX2xHE-_eJsABOi_Oe4nBAtGb27B_WiJjZdl7dC-cwpr9Oq6u390Q0wWpDMDojbM6pQ79dq64x2LdYFcgnGPz_EfqNHmnb-zceHKzMUNRx4R312DNbaKOMG5n6pcteZlu_KE3hSPmYuN1V1hWA8vgkMbzY3TaIriT0PN6Q1E48mdXy4J4_v-jzUzTX6fn-hHB2CKOvG9vtQhfPF4x4JM7hl0MKi_k-LbJT36cKu-ViZ78ZLv1Y8gKYpHCz1ywImw2WrsJklZP3bwuEQuHmaUNpBQA0x91fT5_f1ayr3TJrSizRCJ_WeIGpCV7lGwXlVFDVC_SM64uPQgER0wWhsIqDMz_xU_oEXqDNjGNUj_7VkRd7bKtImXelzo-2y-vsfgnMwtgP3Xxgl96j1tFs2jgoZemtOHJGE410i6l8ov5ZH3Ibz6-rwHB6D-TD2M6atnYSVMkfF7_mzmdeIgfHkDkCRbEIgbW0HIMMp--ohpWUmlCIMrEkiSsusRGEtrJJrGm6y8TezOkEHM5TwYUmU5LS8Sp2IFHpMt5dQVswyJADTj6nggE4RDUbc0G09SGCIoFW-bLW4Jv1SPwL7jM4uNyIt71MulD8P33-H8W9MoIrNKqqq7AZ3WzgvCmHxVezzK0dqBfTeCHV0wCu2v12FV_a3ZEUY6AmNnthpW6Yj7_b7SSN4E_iK1Q8sJtiO4-0crl7l5sOjFUgMdkcyAMJhn39csFV0hfUmEtcCRLHW9HkGx61ti91f6v3Tx96N7nWFeBj_Rigo93vEuNHXpzxNukIEXHKPOrp-hc1YjaqJgfGngpgu0gRWq5dn5LRaUMgIIDmduJtIjjlA1OzjveMPS_scLFLssVRQsnuXQDJIVWEArc38yBuuxpYNuWf2o-gWhE9JwdfSWi00h7TD-mm1UirpFA3cgpQP9MvJOSmqJfyu5WZTZJMObllHmLkHtFStEdY0jYpjkeA-fAm1Qaaa1ONKIjpQavvlsFVWJ21n-AyEs7cBTRqcU2FrF-rKWgPdoR9AMCyDlvSv6fme0oBMQ-MxmDqXgZP4nt_PT2oDXezK4KcI0iyojLYsFuNd0rP-sDZlTcY0u66C8apjiSNAb1xwb9w-Cj4Jk2OXtZ_ygzX7EYzzH_nogbVNeIoVvBwBx1E27RbvAg2WIUqpnE1i3lWneoe0ig93cAqW5IOCs8SN5iHSO4m5eCq02TEbGjoif3kg5-6JEd71Bv3pRbtF8zah2uFYu8fR-awcca6wJgajq9iSa_jaN4l1RraSYQ2mBEeRc4gxk-0ddWdAYgwSkI-Y8kow18B9yGSdlkJad1mOZ1AvKfo0ow18RHTwAjLoKoEyhjpHVueQ0yH9jZtUyG0tFBu0vhmDkh_ZlkxlaXiwF2QiqUzHiEna9fval6YM1BFiE4h0Yy_O2Gk5g-ksrPeR80UgERdxYkUE_0DCQtIncMV7BK4fTjdW5yHAHTF9zxPISk4KBZ4jl7tG12DJIg9MB5ctNiMIZAmK__8sZIPe2AQF4suoyAFh0Ri1atDmIEY21xwp68hKrRsDe7Erb_n_n1Z-__jh06kti_objuE2luiMrZ8R5um6mfNL4Xh7i1dMqDTVl1nnhIi0CfnK4YEmDKjp3kF0pbV9KNEWsrsAMUFoX9IkEBRjMXizm3GkSvsWIS3ik4VRaUJmkikXRrwzYCJOCzdPwM-qBsxNDHnBvaEic4J-thCMu1db4tFuwziyoj678AdO5xIZYk0IK-hBgku5mswX5cF7CpyrA6vQ-Q**eb2201454b8bd2dcb4c314e6565e0151068e75e60fac2cc0c3e833533a11f584*BgpZmzf2qYyZeXmvqZj1RegjsxQhFCxft-64P5heNoA~2; olive-auth=1754609124460'
      },
      body: JSON.stringify({
        "0": {
          json: {
            prompt: tool.prompt,
            dbId: dbId
          }
        }
      })
    });

    if (!appResponse.ok) {
      throw new Error(`App creation failed for "${tool.title}": ${appResponse.status} ${appResponse.statusText}`);
    }

    const app = await appResponse.json();
    const appId = app[0].result.data.json.id;
    console.log(`✅ App created: ${tool.title} (ID: ${appId})`);
  }

  console.log("🎉 Olive integration completed successfully!");
}