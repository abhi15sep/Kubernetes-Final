using BookInfo.Details.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using System.Collections.Generic;
using System.Threading;

namespace BookInfo.Details.Controllers
{
    [ApiController]
    [Route("details")]
    public class DetailsController : ControllerBase
    {
        private static List<string> _RequestIDs = new List<string>();
                
        protected readonly IConfiguration _configuration;
        private readonly ILogger _logger;

        public DetailsController(IConfiguration configuration, ILogger<DetailsController> logger)
        {
            _configuration = configuration;
            _logger = logger;
        }

        [HttpGet("{id}")]
        public IActionResult Get(int id)
        {
            if (_configuration["SERVICE_VERSION"]== "v-unavailable")
            {
                return StatusCode(503);
            }
            if (_configuration["SERVICE_VERSION"] == "v-timeout")
            {
                Thread.Sleep(30 * 1000);
                return StatusCode(500);
            }
            if (_configuration["SERVICE_VERSION"] == "v-timeout-first-call")
            {
                var requestId = Request.Headers["x-request-id"];
                if (!_RequestIDs.Contains(requestId))
                {
                    _logger.LogInformation($"NEW request, ID: {requestId}; will timeout");
                    _RequestIDs.Add(requestId);
                    Thread.Sleep(30 * 1000);
                    return StatusCode(500);
                }
                _logger.LogInformation($"REPEAT request, ID: {requestId}; will respond");
            }
            return Ok(GetDetails(id));
        }

        private BookDetails GetDetails(int id)
        {
            var book = new BookDetails
            {
                Id = id,
                Type = "paperback",
                Publisher = "PublisherA",
                Language = "English"
            };
            if (id==100)
            {
                book.Author = "Elton Stoneman";
                book.Year = 2020;
                book.Pages = 600;
                book.Isbn10 = "SECRET";
                book.Isbn13 = "000-SECRET";
                _logger.LogInformation($"Secret book accessed...");
            }
            else
            {
                book.Author = "William Shakespeare";
                book.Year = 1595;
                book.Pages = 200;
                book.Isbn10 = "1234567890";
                book.Isbn13 = "123-1234567890";
            }
            return book;
        }
    }
}