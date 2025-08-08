export async function createOliveIntegration(structuredOutput: any) {
  const { tool_suggestions, connection_string } = structuredOutput;
  const wosSession = 'Fe26.2*1*02a629a83ed010d7f2cc79ac08c403a51cf45da747d146ad0d857024e30f3963*-MicGr3pmmf_zOPyNh2yAQ*R2uSPRBgebgjWxCLSrPBt_oheblFG-gvdSSQ4ubzB1N-m_Hy8Ik9rqDgLLR43kyxcVY6G70lTFluJI4n0L3JD9tKNXqnWpKISnof8zZZclCdlqZLyfRnzV6vgW6c2ibOmVrR8RL_wElmjiecN8HVX0KqPs9yVT-3Ev1hV-OdoaUVRNPFNFP3kwJ4oID0WLoK9l0PLVrqWUkD5KUX54uhQCfjDRWjRnpJ02HM6ia2eQ_xBgFQR2p1wXvDguEBvq1KJp1sWEPv_EM65O6viHTNcz4-geGC9xfX2KbQGgQLTdSM3Wa9NQRFGCfnYYxg7dxnO6S7KP0LX_hdRJCiJBgt6RMSrQY90Kvh1prYr1AdBka3uYoxHmsL3WoLTNWCfI6fFQSfebnw09eCs_6aSvoMFhVWkAKawIPvS827RBAQz65mZnWsVuPxrRsE1eKvzMIuhpNVGXklT9hblpmRWbUyB2qvgvkh825wEMjHQL4DNwK8mdJykWCVj1-lo5t8DNeCBA66xH_TLncDi-cb7u_Er5IYlrGUSmXnqPS27Uf9qVwZ1Rk_HJCHh1L1sXhwTx8KdQ88gXLbu30IwU6cpuf5mLBdjmBsnSAJFdk1IxVqia7H6SLHNV7mp2uP9jb59ZVPiEdlrDo6Jg8aC72c6dN4JCWubam1ZV4h4M8k5LwL8uCMv813nkg6Qlco8R_R490VOPCTrYI1uqvFSdZa6ZBxPP5zigNzObhvLew7F1DTpPYGxmgp94UGWGHeE-ZJemEJl_ZeglmGjShviRoh98-T03Fa5TnYOnXH1azjxUe4iEV2TTcgX60RxD7Eajsp1O_htMisl-kBFser_1nNzXnzuQkeMQ3TpxheSdK5ZbtD-fNlv0h7qPaAqDAWT8HUl0cCB1scSCgmM8hGxvLprQ9A4_BHcUij4lmcTQ5QMbtZGv_R-OaD4EX2wZyn7hYqFyDkSS86ex1FwVLLtyYWjOSMWMYGu-tSLV7r_VERhrtW0odjPDpl9bc5OjWSr3ce5P9jv5eJf0-0Bqqt4wxa2Mno4OhHbeOhLSrag0eMQZZBOrn0Cso3nKvAcdCcUq3QV8Lk7U_uzExNSzIbfuROqDynCH5MoKoFYGg2ngOHfbq6s2rH2yek6pNcQ87Va8-wz5pIimrOQIARWbSe_uu2pzhEuBoizBeWTu5unMNcyjJ078UCDqFiRb2R6UpT8FkpSLy1D2okKLCpPrZwSOIKktlCwI-92ab0hhSCesSNMq9oIzlqkS6m2EivrxqUEP4twGX3m7hnILhqWE1cc6X5Q7MvuOUqMLs1beaHq8ipSUoLmQf8oZntZ7wzTMySbD3MfHHTtPwmzz5ClaV5Yh75rRewsKX3maAhlkbNEXYZVDeExF3NIU0gpcDYAqGjlqGm5fIT362pDLKlynHFOKhaCsdbrf6hFhKKgPDPINumXaND3AwjyYs8RkqwOhn4-sACZBVGF5JwaQZmCwboDUyqZby-1gUHG03JVx36-YyWWfL7TihXbXoz76pZgKwsZGXRPcP-PTo06OnTk6UnQWs61WyLBF-TknqhSu7fV_0l1lgjiquMhHO4yK6sgJIe7ASZBBJRsQGUhwZtmbUde2qIKLAVM_umltHFDtSR9dv2rGkxdQfU_UtYqr3tm24gKXHyousgZRyckUO19aqC7YiUGmKIAfA3HRDLQL-jlBCRSEbHsddh38ZTjCQieJ7Ypr58lMxn1e7xwLKPooSUlZvXfDljxZBt5-nXBtQWegBhamNqP0owxMzPYVW5xwBbQnmHck3Gc-ibF_kZrZY8NSAaAZqN9-P18RW8EdWtPfDhQ2s6m44pwHxEqyTgxsZStXbzaVov9z8GsSb2TeILd-m3xpE3-g**0f35c606cfd3db060fd8a9aecfb4c0ac8f0128c3852de92728312dbb736b61ea*XhoCoTPpBPgTKJia7ywtEtmAWTFQKHXEBCAWJmQtz2U~2';
  const oliveAuth = '1754620032116';

  console.log("🫒 Starting Olive integration...");

  // Step 1: Create database connection
  console.log("Creating database connection...");
  const dbResponse = await fetch('http://dev.fromolive.com:3001/trpc/database.create?batch=1', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Cookie': `wos-session=${wosSession}; olive-auth=${oliveAuth}`
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
        'Cookie': `wos-session=${wosSession}; olive-auth=${oliveAuth}`
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