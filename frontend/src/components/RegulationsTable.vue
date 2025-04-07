<template>
  <div class="regulations-container">
    <table class="data-table">
      <thead>
        <tr>
          <th><i class="fas fa-gavel"></i>Regulation Name</th>
          <th><i class="fas fa-info-circle"></i>Details</th>
          <th v-if="hasColumn('storage_gal_min')"><i class="fas fa-tank"></i>Minimum Storage (Gal)</th>
          <th v-if="hasColumn('storage_gal_max')"><i class="fas fa-tank"></i>Maximum Storage (Gal)</th>
          <th v-if="hasColumn('safety_distance_ft')"><i class="fas fa-ruler"></i>Safety Distance (ft)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.regulation_name">
          <td>{{ item.regulation_name }}</td>
          <td>{{ item.regulation_info }}</td>
          <td v-if="hasColumn('storage_gal_min')">{{ $formatNumber(item.storage_gal_min) }}</td>
          <td v-if="hasColumn('storage_gal_max')">{{ $formatNumber(item.storage_gal_max) }}</td>
          <td v-if="hasColumn('safety_distance_ft')">{{ $formatNumber(item.safety_distance_ft) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "RegulationsTable",
  props: {
    items: {
      type: Array,
      required: true,
    }
  },
  methods: {
    hasColumn(column) {
      return this.items.some(item => column in item);
    },
  },
};
</script>

<style scoped>
.regulations-container {
  margin-bottom: 30px;
  color: #ddd;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  overflow: hidden;
}

.data-table th,
.data-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.data-table th {
  background-color: rgba(255, 255, 255, 0.05);
  font-weight: 600;
  color: #64ffda;
  white-space: nowrap;
}

.data-table th i {
  margin-right: 8px;
  width: 16px;
  text-align: center;
  opacity: 0.8;
}

.data-table tbody tr {
  transition: background-color 0.2s ease;
}

.data-table tbody tr:nth-child(even) {
  background-color: rgba(255, 255, 255, 0.03);
}

.data-table tbody tr:hover {
  background-color: rgba(100, 255, 218, 0.05);
}

.data-table td {
  color: #ddd;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .data-table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }

  .data-table th,
  .data-table td {
    padding: 10px 12px;
  }
}
</style>
