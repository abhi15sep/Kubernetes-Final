using System;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace Numbers.Api.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class RngController : ControllerBase
    {
        private static Random _Random = new Random();
        private static int _CallCount;
        private static int _FailCallCount = 0;

        private readonly ILogger<RngController> _logger;
        private readonly IConfiguration _configuration;

        public RngController(ILogger<RngController> logger, IConfiguration configuration)
        {
            _logger = logger;
            _configuration = configuration;
            if (_FailCallCount == 0)
            {
                _FailCallCount = int.Parse(_configuration["FailAfter"]);
            }
        }

        [HttpGet]
        public IActionResult Get()
        {
            if (Status.Healthy == false)
            {
                _CallCount = 0;
                _logger.LogWarning("Unhealthy!");
                return StatusCode(500);
            }
            else
            {
                _CallCount++;
                if (_CallCount >= _FailCallCount)
                {
                    Status.Healthy = false;
                }
                var n = _Random.Next(0,100);
                _logger.LogDebug($"Returning random number: {n}");
                return Ok(n);
            }
        }
    }
}
