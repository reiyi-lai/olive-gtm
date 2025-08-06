import aiohttp
import asyncio
import json
from typing import Dict, Any, Optional, List
from utils.logger import logger
from urllib.parse import urljoin, urlencode

1
class OliveService:
    """
    Service for integrating with Olive platform.
    Handles database connection, schema refresh, and prompt generation.
    """
    
    def __init__(self, backend_url: str = "http://localhost:3000", frontend_url: str = "http://localhost:3001"):
        self.backend_url = backend_url
        self.frontend_url = frontend_url
        self.trpc_endpoint = f"{backend_url}/trpc"
    
    async def integrate_with_olive(
        self, 
        connection_string: str, 
        database_name: str = None,
        suggestions_count: int = 4
    ) -> Dict[str, Any]:
        """
        Complete integration with Olive platform.
        
        Args:
            connection_string: Neon PostgreSQL connection string
            database_name: Name for the database in Olive
            suggestions_count: Number of prompt suggestions to generate
            
        Returns:
            Dict containing integration results and Olive URLs
        """
        if not database_name:
            database_name = f"Neon DB {asyncio.get_event_loop().time()}"
        
        try:
            logger.info("🔌 Starting Olive integration...")
            
            # 1. Connect database to Olive
            database = await self._connect_database(database_name, connection_string)
            logger.info(f"✅ Database connected to Olive: {database.get('id')}")
            
            # 2. Refresh schema to analyze tables
            await self._refresh_schema(database['id'])
            logger.info("✅ Schema refreshed in Olive")
            
            # 3. Generate prompt suggestions
            suggestions = await self._generate_suggestions(database['id'], suggestions_count)
            logger.info(f"✅ Generated {len(suggestions)} prompt suggestions")
            
            return {
                'success': True,
                'database': database,
                'suggestions': suggestions,
                'frontend_url': f"{self.frontend_url}?db={database['id']}",
                'admin_url': f"{self.backend_url}/panel",
                'database_id': database['id']
            }
            
        except Exception as e:
            logger.error(f"❌ Olive integration failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'database': None,
                'suggestions': []
            }
    
    async def _connect_database(self, name: str, connection_string: str) -> Dict[str, Any]:
        """Connect database to Olive via tRPC API."""
        return await self._call_trpc_api(
            'database.create',
            {
                'name': name,
                'connectionString': connection_string,
                'sslMode': 'require'
            },
            method='POST'
        )
    
    async def _refresh_schema(self, database_id: str) -> Dict[str, Any]:
        """Refresh database schema in Olive."""
        return await self._call_trpc_api(
            'database.refreshSchema',
            {'id': database_id},
            method='POST'
        )
    
    async def _generate_suggestions(self, database_id: str, count: int = 4) -> List[Dict[str, Any]]:
        """Generate prompt suggestions from Olive."""
        return await self._call_trpc_api(
            'database.generatePromptSuggestions',
            {'dbId': database_id, 'count': count},
            method='GET'
        )
    
    async def create_app_from_prompt(self, database_id: str, prompt: str) -> Dict[str, Any]:
        """Create an Olive app from a prompt."""
        return await self._call_trpc_api(
            'app.create',
            {
                'prompt': prompt,
                'dbId': database_id
            },
            method='POST'
        )
    
    async def _call_trpc_api(self, procedure: str, input_data: Dict[str, Any] = None, method: str = 'GET') -> Any:
        """
        Make tRPC API calls to Olive backend.
        
        Args:
            procedure: tRPC procedure name (e.g., 'database.create')
            input_data: Data to send with the request
            method: HTTP method ('GET' or 'POST')
        """
        url = f"{self.trpc_endpoint}/{procedure}"
        
        # Set up headers with authentication
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Add authentication cookies as required by Olive
        cookies = {
            'olive-auth': '1754425963429',
            'wos-session': 'Fe26.2*1*87e3b08e598ed088c6622a5aade27fca3e1bba803508f667ba8536774fb4a6ce*yEMnZGCVvcvHkj7MiKk8ZQ*Xzuwt5a2vJECTjdkDjHzzGCbyOQjaBdGI2lnspnGtyMAfnvn0YdI9KvipiCKmp4vOCVSP9VEZpC2VxvRttrwyTgrU5U_eSu9FA7kqX4m1G7eB9NznaQh52QcWgAve4HzpBSI45pjWVnrutXep4AM0bz2fGhNmkMki0uaITKny8CJSSqLGWJgAJoT72pQOz-dCdkVW7a9jK_cWAmRvVt3coSSsIN_JVJh5ZtjZOAuVDDXzQ5zvitue0gwUik8oiDON-K3mxe1grjkSZgSm7nytjARrf9z5Lfj97vM0MAOhCHAipIAAWB3empC1QgfxFZ1ZinHp9vZ-aKq-H4OaLMNwZfZibS45a1tQft3tQsWsqCmEcIQ-2SUaq4Doyl8m2etCUtgvLBKIcY-IhpXK0R-6TMGungz1Ows6vQo1qt3WXVnyAxhmZH5ZgFvmMOxOi_-ZpoVGjVjfQNuPJSmB0rLLvCZu_343iF-bstMQdwSKNmppG7373HkrVd1am3aiYm8vY8j2NzGcDMYfv-9G5TPTSHGNSWThmE0Q70bTeYQEnXltxknCMNDuy15Q75MXVJblS07HE2qEVp19qcdJMiXdJoNEIHaHGkUWVFbbebiOjO62gesuSRoMJWSGp-Dvlmr0PskP6rcT9Lh8KY6Pq8qdgJFDWpx2c_8oYdPeF9CiooP8sz0PaUPhjZKGDU7b2gjiTIc1vTwGR7xKdw7mv1Z2WHadAPtZLyvC16HGXNYCTNt0UCiMvcKliREgci4xZnsxVzUOcz_uhdcXZvYRSwLQQymITt4tgz61Nv5yGAEndpxdpM3y87VwRRkJtNFpAIGoYyr9o9_uGy9FDNkGvhP41rUmawzcwThYkjGHEuaJvMHnddR5UrsxMh2tAHbMsf_UMaMfGJ6e7GOhxF01DpAFSFyNKD3vK2YHoVzpnKCwjykuS67gDwC7E6etavNkDAiATVj2CCGF1yB6ZCb2SVPWoXswqASD_JRiPZCdJ7opNzgRectjEp6b6XQHr6xJxnBnPrXhmjIYWWdF7DzU2J50wyisb-FdQzXNgJbEm5axFPafLLnnS_IpkhEM5GGtbsb7uRw3MXtzxMWM6S2roMIKCktSLiwvOkIvlPjK9S1XVUQxIZ1iO_PXCcxibFp7rsf9N_H_tIRehV2NjS7pbEuloh7sM0JpH3-DVEpYTJzvZ9b4mpoTvx6Gk6T5hGtBAXCQT3vlo9PAk0TjU5ihuSVJsEUHI8qlumnzd_H6rct7gOS8PRJ0QH57AWKoeoTdZYX8Qy1jlPbQwOMTr5rMcAF-P0IJpm3oGELgAnDqWxW3tzO07E7-t9EEfaq7AZm7ZzO4zDMr1TllVd8hBJ_mwmoRs6WXsoVt_Blmomd3X1wtb3nLn_0jHIP9GbU9xHwg4vvyHRQw3N-wMBpKBQRVe36jcy3yFtdRil5SDlCVA5kY1GgCuR6tpUTGOKTSGCmrBdo40urndU2gG9yQzVnNutxJG5tR8z-ZKauJ2bEfNKltC0BIzHhnJTtSSXrBUFR7wLtJiIz1Q3cKIAMY9hKDHJvn4TlxpOy-3JP1l_6mZ9dUDQ**2705c1412acda7fe7c1ec3c6143e1242b3830f54f17b39145b35ca9500645e46*OBnv6WcAmCsP81eCgdZARDGGCff7EoFXg4xmRCp51is~2'
        }
        
        try:
            # Configure session with cookies (equivalent to credentials: "include")
            cookie_jar = aiohttp.CookieJar()
            for name, value in cookies.items():
                cookie_jar.update_cookies({name: value})
                
            connector = aiohttp.TCPConnector()
            async with aiohttp.ClientSession(
                connector=connector,
                cookie_jar=cookie_jar,
                headers=headers
            ) as session:
                if method == 'GET' and input_data:
                    # For GET requests, encode input as query parameter
                    query_params = {'input': json.dumps(input_data)}
                    url = f"{url}?{urlencode(query_params)}"
                    
                    async with session.get(url) as response:
                        return await self._handle_response(response, procedure)
                        
                elif method == 'POST':
                    # For POST requests, send input in body with exact format from user
                    payload = input_data or {}
                    # Add the additional fields that Olive expects
                    if procedure == 'database.create':
                        payload.setdefault('sslData', {})
                        payload.setdefault('bastionHostData', None)
                    
                    async with session.post(
                        url, 
                        json=payload
                    ) as response:
                        return await self._handle_response(response, procedure)
                        
                else:
                    # GET request without input
                    async with session.get(url) as response:
                        return await self._handle_response(response, procedure)
                        
        except aiohttp.ClientError as e:
            logger.error(f"Network error calling {procedure}: {str(e)}")
            raise Exception(f"Failed to connect to Olive backend: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error calling {procedure}: {str(e)}")
            raise
    
    async def _handle_response(self, response: aiohttp.ClientResponse, procedure: str) -> Any:
        """Handle API response and extract data."""
        if not response.ok:
            error_text = await response.text()
            logger.error(f"API call to {procedure} failed: {response.status} {error_text}")
            raise Exception(f"API call failed: {response.status} {response.reason}")
        
        try:
            data = await response.json()
            # tRPC responses are usually wrapped in { result: { data: ... } }
            if isinstance(data, dict):
                if 'result' in data and 'data' in data['result']:
                    return data['result']['data']
                elif 'result' in data:
                    return data['result']
                else:
                    return data
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from {procedure}: {str(e)}")
            raise Exception(f"Invalid response from Olive API: {str(e)}")
    
    def get_frontend_url(self, database_id: str) -> str:
        """Get the frontend URL for a specific database."""
        return f"{self.frontend_url}?db={database_id}"
    
    def get_admin_url(self) -> str:
        """Get the admin panel URL."""
        return f"{self.backend_url}/panel"
    
    async def health_check(self) -> bool:
        """Check if Olive backend is running and accessible."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/health", timeout=5) as response:
                    return response.ok
        except:
            return False