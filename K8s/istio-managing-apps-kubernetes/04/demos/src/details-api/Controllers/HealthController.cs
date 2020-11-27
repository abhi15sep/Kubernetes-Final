using Microsoft.AspNetCore.Mvc;

namespace BookInfo.Details.Controllers
{
    [ApiController]
    [Route("health")]
    public class HealthController : ControllerBase
    {
        [HttpGet]
        public IActionResult Get()
        {
            return Ok(new { status = "Details is healthy" });
        }
    }
}