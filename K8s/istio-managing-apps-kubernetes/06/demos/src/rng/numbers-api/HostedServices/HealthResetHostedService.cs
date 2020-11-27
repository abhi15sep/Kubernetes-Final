using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace Numbers.Api
{
    public class HealthResetHostedService : IHostedService, IDisposable
    {

        private readonly ILogger _logger;
        private Timer _timer;

        public HealthResetHostedService(ILogger<HealthResetHostedService> logger)
        {
            _logger = logger;
        }

        public Task StartAsync(CancellationToken cancellationToken)
        {
            _logger.LogInformation("HealthResetHostedService is starting.");

            _timer = new Timer(ResetHealth, null, TimeSpan.Zero, 
                TimeSpan.FromSeconds(30));

            return Task.CompletedTask;
        }

        private void ResetHealth(object state)
        {
            if (Status.Healthy == false)
            {
                Status.Healthy = true;
                _logger.LogInformation("STATUS RESET! Healthy again.");
            }
        }

        public Task StopAsync(CancellationToken cancellationToken)
        {
            _logger.LogInformation("HealthResetHostedService is stopping.");
            _timer?.Change(Timeout.Infinite, 0);
            return Task.CompletedTask;
        }

        public void Dispose()
        {
            _timer?.Dispose();
        }
    }
}