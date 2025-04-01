<template>
  <div class="app">
    <header class="header">
      <h1>Busca de Operadoras</h1>
      <button class="settings-button" @click="showSettings = true">
        <span class="settings-icon">⚙️</span> Settings
      </button>
    </header>
    
    <main class="main">
      <div class="search-container">
        <div class="search-input-group">
          <input 
            v-model="searchQuery" 
            @keyup.enter="handleSearch"
            type="text" 
            placeholder="Buscar operadoras..."
            class="search-input"
          >
          <button 
            class="search-button" 
            @click="handleSearch"
            :disabled="searchQuery.length < 3"
          >
            Buscar
          </button>
        </div>
        <div v-if="searchQuery && searchQuery.length < 3" class="search-hint">
          Digite pelo menos 3 caracteres para pesquisar
        </div>
      </div>

      <div v-if="loading" class="loading">
        Carregando...
      </div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <div v-else class="results">
        <div v-if="hasSearched" class="search-info">
          Encontrados {{ results.length }} resultados para "{{ lastSearchQuery }}"
        </div>
        
        <div v-if="results.length === 0 && hasSearched" class="no-results">
          Nenhum resultado encontrado para "{{ lastSearchQuery }}"
        </div>
        
        <div v-else-if="results.length > 0" class="results-grid">
          <div v-for="operadora in results" :key="operadora.Registro_ANS" class="operadora-card">
            <h3>{{ operadora.Razao_Social }}</h3>
            <p><strong>Nome Fantasia:</strong> {{ operadora.Nome_Fantasia }}</p>
            <p><strong>Registro ANS:</strong> {{ operadora.Registro_ANS }}</p>
            <p><strong>CNPJ:</strong> {{ operadora.CNPJ }}</p>
            <p><strong>Modalidade:</strong> {{ operadora.Modalidade }}</p>
            <p><strong>Cidade:</strong> {{ operadora.Cidade }} - {{ operadora.UF }}</p>
            <p><strong>Telefone:</strong> ({{ operadora.DDD }}) {{ operadora.Telefone }}</p>
            <p><strong>Email:</strong> {{ operadora.Endereco_eletronico }}</p>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal de Configurações -->
    <div v-if="showSettings" class="modal-overlay" @click="showSettings = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Configurações de Pesquisa</h2>
          <button class="close-button" @click="showSettings = false">&times;</button>
        </div>
        <div class="modal-body">
          <p>Selecione as colunas para incluir na pesquisa:</p>
          <div class="checkbox-list">
            <label v-for="column in availableColumns" :key="column" class="checkbox-label">
              <input 
                type="checkbox" 
                v-model="selectedColumns" 
                :value="column"
              >
              {{ column }}
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button class="save-button" @click="saveSettings">Salvar Configurações</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      searchQuery: '',
      lastSearchQuery: '',
      results: [],
      loading: false,
      error: null,
      showSettings: false,
      availableColumns: [],
      selectedColumns: [],
      hasSearched: false
    }
  },
  async created() {
    await this.loadSearchSettings();
  },
  methods: {
    async loadSearchSettings() {
      try {
        const response = await fetch('http://localhost:5000/api/search_settings', {
          headers: {
            'Accept': 'application/json'
          }
        });
        if (!response.ok) {
          throw new Error('Failed to load search settings');
        }
        const data = await response.json();
        this.availableColumns = data.columns;
        this.selectedColumns = data.selected_columns;
      } catch (err) {
        console.error('Error loading search settings:', err);
        this.error = 'Error loading search settings';
      }
    },
    async saveSettings() {
      try {
        const response = await fetch('http://localhost:5000/api/search_settings', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            selected_columns: this.selectedColumns
          })
        });
        
        if (!response.ok) {
          throw new Error('Failed to save settings');
        }
        
        this.showSettings = false;
        // Refresh search if there's an active query
        if (this.searchQuery.length >= 3) {
          this.handleSearch();
        }
      } catch (err) {
        console.error('Error saving search settings:', err);
        this.error = 'Error saving search settings';
      }
    },
    async handleSearch() {
      if (this.searchQuery.length < 3) {
        return;
      }

      this.loading = true;
      this.error = null;
      this.lastSearchQuery = this.searchQuery;
      this.results = [];  // Limpar resultados anteriores

      try {
        // console.log('Pesquisando por:', this.searchQuery);
        
        const response = await fetch(`http://localhost:5000/api/search?q=${encodeURIComponent(this.searchQuery)}`, {
          headers: {
            'Accept': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error('Falha na requisição de pesquisa');
        }

        const responseData = await response.json();
        
        // console.log('Resposta recebida:', {
        //   responseType: typeof response,
        //   dataType: typeof responseData,
        //   data: responseData
        // });

        if (!responseData || !responseData.data) {
          throw new Error('Nenhum dado recebido na resposta');
        }

        if (!Array.isArray(responseData.data)) {
          console.error('Estrutura de dados inválida:', responseData);
          throw new Error('Formato de resposta inválido: esperado um array de resultados');
        }

        this.results = responseData.data;
        // console.log('Pesquisa concluída:', {
        //   query: this.lastSearchQuery,
        //   resultsCount: this.results.length
        // });
      } catch (err) {
        console.error('Erro na pesquisa:', err);
        this.error = err.message || 'Erro ao buscar resultados. Por favor, tente novamente.';
        this.results = [];
      } finally {
        this.loading = false;
        this.hasSearched = true;
      }
    }
  }
}
</script>

<style>
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.settings-button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.settings-button:hover {
  background-color: #45a049;
}

.search-container {
  margin-bottom: 30px;
}

.search-input-group {
  display: flex;
  gap: 10px;
}

.search-input {
  flex: 1;
  padding: 12px 20px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #4CAF50;
}

.search-button {
  padding: 12px 24px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #45a049;
}

.loading, .error, .no-results {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

.error {
  color: #f44336;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.operadora-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.operadora-card:hover {
  transform: translateY(-2px);
}

.operadora-card h3 {
  margin: 0 0 15px 0;
  color: #333;
}

.operadora-card p {
  margin: 8px 0;
  color: #666;
}

.operadora-card strong {
  color: #333;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.modal-body {
  margin-bottom: 20px;
}

.checkbox-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  margin-top: 10px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
}

.save-button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-button:hover {
  background-color: #45a049;
}

.search-hint {
  color: #666;
  font-size: 14px;
  margin-top: 8px;
}

.search-info {
  text-align: center;
  margin-bottom: 20px;
  color: #666;
}

.search-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style> 