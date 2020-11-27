FROM mcr.microsoft.com/dotnet/core/sdk:3.1.101 AS sdk
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs

FROM sdk as builder
WORKDIR /src

COPY Numbers.Web.csproj .
RUN dotnet restore

COPY . .
RUN dotnet publish -c Release -o /out Numbers.Web.csproj

# app image
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1.1

ENV RngApi:Url=http://numbers-api/rng

ENTRYPOINT ["dotnet", "/app/Numbers.Web.dll"]

WORKDIR /app
COPY --from=builder /out/ .