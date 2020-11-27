FROM mcr.microsoft.com/dotnet/core/sdk:3.1.101 AS builder

WORKDIR /src
COPY Numbers.Api.csproj .
RUN dotnet restore

COPY . .
RUN dotnet publish -c Release -o /out Numbers.Api.csproj

# app image
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1.1

ENTRYPOINT ["dotnet", "/app/Numbers.Api.dll"]

WORKDIR /app
COPY --from=builder /out/ .