// Configurações da API
const API_CONFIG = {
    STATUS_SERVICE: 'http://localhost:8001',
    TELEMETRY_SERVICE: 'http://localhost:8002',
    UPDATE_INTERVAL: 3000 // 3 segundos
};

// Estado global da aplicação
let currentSatellite = null;
let telemetryUpdateInterval = null;
let temperatureChart = null;
let batteryChart = null;
let telemetryHistory = {
    temperature: [],
    battery: [],
    timestamps: []
};

// Função para mostrar/esconder loading
function showLoading(show = true) {
    const overlay = document.getElementById('loading-overlay');
    if (show) {
        overlay.classList.add('show');
    } else {
        overlay.classList.remove('show');
    }
}

// Função para fazer requisições HTTP
async function makeRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error;
    }
}

// Função para verificar status dos serviços
async function checkServicesHealth() {
    try {
        const statusHealth = await makeRequest(`${API_CONFIG.STATUS_SERVICE}/health`);
        const telemetryHealth = await makeRequest(`${API_CONFIG.TELEMETRY_SERVICE}/health`);
        
        updateServiceStatus(true, true);
        return true;
    } catch (error) {
        console.warn('Alguns serviços podem não estar disponíveis:', error);
        updateServiceStatus(false, false);
        return false;
    }
}

// Função para atualizar indicadores de status dos serviços
function updateServiceStatus(statusService, telemetryService) {
    const statusDots = document.querySelectorAll('.status-dot');
    
    if (statusDots[0]) {
        statusDots[0].classList.toggle('active', statusService);
    }
    if (statusDots[1]) {
        statusDots[1].classList.toggle('active', telemetryService);
    }
}

// Função para carregar lista de satélites
async function loadSatellites() {
    try {
        showLoading(true);
        
        const satellites = await makeRequest(`${API_CONFIG.STATUS_SERVICE}/satelites`);
        displaySatellites(satellites);
        
    } catch (error) {
        console.error('Erro ao carregar satélites:', error);
        document.getElementById('satellites-grid').innerHTML = 
            '<div style="text-align: center; color: #ff4444; padding: 40px;">Erro ao carregar dados dos satélites</div>';
    } finally {
        showLoading(false);
    }
}

// Função para exibir satélites na lista
function displaySatellites(satellites) {
    const grid = document.getElementById('satellites-grid');
    
    grid.innerHTML = satellites.map(satellite => `
        <div class="satellite-card" onclick="selectSatellite(${satellite.id}, '${satellite.name}')">
            <h3>
                <i class="fas fa-satellite"></i>
                ${satellite.name}
            </h3>
            <div class="satellite-info">
                <div class="info-item">
                    <span class="info-label">Status:</span>
                    <span class="status-badge ${satellite.status ? 'active' : 'inactive'}">
                        ${satellite.status ? 'Ativo' : 'Inativo'}
                    </span>
                </div>
                <div class="info-item">
                    <span class="info-label">Órbita:</span>
                    <span class="info-value">${satellite.orbit_type}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Tempo Operacional:</span>
                    <span class="info-value">${formatOperationalTime(satellite.operational_time)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Última Atualização:</span>
                    <span class="info-value">${formatDateTime(satellite.last_update)}</span>
                </div>
            </div>
        </div>
    `).join('');
}

// Função para formatar tempo operacional
function formatOperationalTime(hours) {
    const years = Math.floor(hours / 8760);
    const days = Math.floor((hours % 8760) / 24);
    const remainingHours = Math.floor(hours % 24);
    
    if (years > 0) {
        return `${years} anos, ${days} dias`;
    } else if (days > 0) {
        return `${days} dias, ${remainingHours}h`;
    } else {
        return `${remainingHours} horas`;
    }
}

// Função para formatar data/hora
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR');
}

// Função para selecionar um satélite
async function selectSatellite(satelliteId, satelliteName) {
    currentSatellite = { id: satelliteId, name: satelliteName };
    
    // Atualizar título da página de monitoramento
    document.getElementById('monitoring-title').innerHTML = 
        `<i class="fas fa-satellite"></i> ${satelliteName}`;
    
    // Mostrar página de monitoramento
    showMonitoringPage();
    
    // Carregar dados iniciais
    await loadSatelliteData();
    
    // Iniciar atualização automática
    startTelemetryUpdates();
}

// Função para mostrar página de monitoramento
function showMonitoringPage() {
    document.getElementById('satellite-list').classList.remove('active');
    document.getElementById('satellite-monitoring').classList.add('active');
}

// Função para mostrar lista de satélites
function showSatelliteList() {
    document.getElementById('satellite-monitoring').classList.remove('active');
    document.getElementById('satellite-list').classList.add('active');
    
    // Parar atualizações automáticas
    stopTelemetryUpdates();
    
    // Limpar gráficos
    if (temperatureChart) {
        temperatureChart.destroy();
        temperatureChart = null;
    }
    if (batteryChart) {
        batteryChart.destroy();
        batteryChart = null;
    }
    
    // Limpar histórico
    telemetryHistory = {
        temperature: [],
        battery: [],
        timestamps: []
    };
}

// Função para carregar dados do satélite
async function loadSatelliteData() {
    if (!currentSatellite) return;
    
    try {
        showLoading(true);
        
        // Carregar dados de status
        const statusData = await makeRequest(`${API_CONFIG.STATUS_SERVICE}/satelites/${currentSatellite.id}`);
        displayStatusData(statusData);
        
        // Carregar dados de telemetria
        const telemetryData = await makeRequest(`${API_CONFIG.TELEMETRY_SERVICE}/telemetria/${currentSatellite.id}/historico?limit=20`);
        displayTelemetryData(telemetryData);
        
        // Inicializar gráficos
        initializeCharts();
        
    } catch (error) {
        console.error('Erro ao carregar dados do satélite:', error);
    } finally {
        showLoading(false);
    }
}

// Função para exibir dados de status
function displayStatusData(statusData) {
    const statusCard = document.getElementById('status-card');
    
    statusCard.innerHTML = `
        <div class="status-item-card">
            <h4>Status</h4>
            <div class="value">
                <span class="status-badge ${statusData.status ? 'active' : 'inactive'}">
                    ${statusData.status ? 'Ativo' : 'Inativo'}
                </span>
            </div>
        </div>
        <div class="status-item-card">
            <h4>Tipo de Órbita</h4>
            <div class="value">${statusData.orbit_type}</div>
        </div>
        <div class="status-item-card">
            <h4>Tempo Operacional</h4>
            <div class="value">${formatOperationalTime(statusData.operational_time)}</div>
        </div>
        <div class="status-item-card">
            <h4>Última Atualização</h4>
            <div class="value">${formatDateTime(statusData.last_update)}</div>
        </div>
    `;
}

// Função para exibir dados de telemetria
function displayTelemetryData(telemetryData) {
    if (!telemetryData || telemetryData.length === 0) return;
    
    // Pegar o último registro
    const latestData = telemetryData[0];
    
    // Atualizar valores atuais
    document.getElementById('current-temperature').textContent = `${latestData.temperature.toFixed(1)}°C`;
    document.getElementById('current-battery').textContent = `${latestData.battery_level.toFixed(1)}%`;
    document.getElementById('current-latitude').textContent = `${latestData.latitude.toFixed(4)}°`;
    document.getElementById('current-longitude').textContent = `${latestData.longitude.toFixed(4)}°`;
    document.getElementById('current-altitude').textContent = `${latestData.altitude.toFixed(1)} km`;
    document.getElementById('last-update').textContent = formatDateTime(latestData.timestamp);
    
    // Preparar dados para gráficos
    telemetryHistory = {
        temperature: telemetryData.slice(0, 10).reverse().map(d => d.temperature),
        battery: telemetryData.slice(0, 10).reverse().map(d => d.battery_level),
        timestamps: telemetryData.slice(0, 10).reverse().map(d => 
            new Date(d.timestamp).toLocaleTimeString('pt-BR', { 
                hour: '2-digit', 
                minute: '2-digit' 
            })
        )
    };
}

// Função para inicializar gráficos
function initializeCharts() {
    // Configuração comum dos gráficos
    const chartConfig = {
        type: 'line',
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(0, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#b0b0b0'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(0, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#b0b0b0'
                    }
                }
            }
        }
    };
    
    // Gráfico de temperatura
    const tempCtx = document.getElementById('temperatureChart').getContext('2d');
    temperatureChart = new Chart(tempCtx, {
        ...chartConfig,
        data: {
            labels: telemetryHistory.timestamps,
            datasets: [{
                label: 'Temperatura',
                data: telemetryHistory.temperature,
                borderColor: '#ff6b6b',
                backgroundColor: 'rgba(255, 107, 107, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        }
    });
    
    // Gráfico de bateria
    const batteryCtx = document.getElementById('batteryChart').getContext('2d');
    batteryChart = new Chart(batteryCtx, {
        ...chartConfig,
        data: {
            labels: telemetryHistory.timestamps,
            datasets: [{
                label: 'Bateria',
                data: telemetryHistory.battery,
                borderColor: '#4ecdc4',
                backgroundColor: 'rgba(78, 205, 196, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        }
    });
}

// Função para atualizar gráficos
function updateCharts(newData) {
    if (!temperatureChart || !batteryChart) return;
    
    // Adicionar novos dados
    telemetryHistory.temperature.push(newData.temperature);
    telemetryHistory.battery.push(newData.battery_level);
    telemetryHistory.timestamps.push(
        new Date(newData.timestamp).toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        })
    );
    
    // Manter apenas os últimos 10 pontos
    if (telemetryHistory.temperature.length > 10) {
        telemetryHistory.temperature.shift();
        telemetryHistory.battery.shift();
        telemetryHistory.timestamps.shift();
    }
    
    // Atualizar gráficos
    temperatureChart.data.labels = telemetryHistory.timestamps;
    temperatureChart.data.datasets[0].data = telemetryHistory.temperature;
    temperatureChart.update('none');
    
    batteryChart.data.labels = telemetryHistory.timestamps;
    batteryChart.data.datasets[0].data = telemetryHistory.battery;
    batteryChart.update('none');
}

// Função para iniciar atualizações automáticas
function startTelemetryUpdates() {
    if (telemetryUpdateInterval) {
        clearInterval(telemetryUpdateInterval);
    }
    
    telemetryUpdateInterval = setInterval(async () => {
        if (!currentSatellite) return;
        
        try {
            // Buscar último dado de telemetria
            const latestTelemetry = await makeRequest(
                `${API_CONFIG.TELEMETRY_SERVICE}/telemetria/${currentSatellite.id}/ultimo`
            );
            
            // Atualizar valores na interface
            document.getElementById('current-temperature').textContent = `${latestTelemetry.temperature.toFixed(1)}°C`;
            document.getElementById('current-battery').textContent = `${latestTelemetry.battery_level.toFixed(1)}%`;
            document.getElementById('current-latitude').textContent = `${latestTelemetry.latitude.toFixed(4)}°`;
            document.getElementById('current-longitude').textContent = `${latestTelemetry.longitude.toFixed(4)}°`;
            document.getElementById('current-altitude').textContent = `${latestTelemetry.altitude.toFixed(1)} km`;
            document.getElementById('last-update').textContent = formatDateTime(latestTelemetry.timestamp);
            
            // Atualizar gráficos
            updateCharts(latestTelemetry);
            
        } catch (error) {
            console.error('Erro ao atualizar telemetria:', error);
        }
    }, API_CONFIG.UPDATE_INTERVAL);
}

// Função para parar atualizações automáticas
function stopTelemetryUpdates() {
    if (telemetryUpdateInterval) {
        clearInterval(telemetryUpdateInterval);
        telemetryUpdateInterval = null;
    }
}

// Função para inicializar a aplicação
async function initializeApp() {
    console.log('Inicializando Satellite Monitoring System...');
    
    // Verificar saúde dos serviços
    await checkServicesHealth();
    
    // Carregar lista de satélites
    await loadSatellites();
    
    console.log('Aplicação inicializada com sucesso!');
}

// Event listeners
document.addEventListener('DOMContentLoaded', initializeApp);

// Função para recarregar dados (útil para debugging)
window.reloadData = function() {
    if (currentSatellite) {
        loadSatelliteData();
    } else {
        loadSatellites();
    }
};
