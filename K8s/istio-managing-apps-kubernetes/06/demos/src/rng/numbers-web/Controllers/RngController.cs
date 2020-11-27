using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RestSharp;

namespace Numbers.Web.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class RngController : ControllerBase
    {
        private readonly ILogger _logger;
        private readonly IConfiguration _configuration;

        public RngController(ILogger<RngController> logger, IConfiguration configuration)
        {
            _logger = logger;
            _configuration = configuration;
        }

        [HttpGet]
        public IActionResult Get()
        {
            var client = new RestClient(_configuration["RngApi:Url"]);
            var request = new RestRequest();
            var response = client.Execute(request);
            if (!response.IsSuccessful)
            {
                return StatusCode(500, "Service call failed");
            }
            return Ok(int.Parse(response.Content));
        }
    }
}
