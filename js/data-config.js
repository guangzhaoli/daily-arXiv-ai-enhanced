/**
 * Data Source Configuration
 *
 * Prefer resolving the current GitHub Pages repository at runtime so forks
 * continue to work even if CI has not injected repository metadata yet.
 */

const DATA_CONFIG = {
    /**
     * GitHub repository owner (username)
     * Can be injected by GitHub Actions, but runtime detection takes precedence.
     */
    repoOwner: 'guangzhaoli',

    /**
     * GitHub repository name
     * Can be injected by GitHub Actions, but runtime detection takes precedence.
     */
    repoName: 'daily-arXiv-ai-enhanced',

    /**
     * Fallback upstream repository for local previews only
     */
    fallbackRepoOwner: 'dw-dengwei',
    fallbackRepoName: 'daily-arXiv-ai-enhanced',

    /**
     * Data branch name
     * Can be injected by GitHub Actions. Falls back to 'data'.
     */
    dataBranch: 'data',
    fallbackDataBranch: 'data',

    isPlaceholder: function(value) {
        return typeof value !== 'string' || value.startsWith('PLACEHOLDER_');
    },

    getConfiguredRepository: function() {
        if (this.isPlaceholder(this.repoOwner) || this.isPlaceholder(this.repoName)) {
            return null;
        }

        return {
            owner: this.repoOwner,
            name: this.repoName
        };
    },

    getRuntimeRepository: function() {
        if (typeof window === 'undefined' || !window.location) {
            return null;
        }

        const { hostname, pathname } = window.location;
        if (!hostname.endsWith('.github.io')) {
            return null;
        }

        const owner = hostname.replace(/\.github\.io$/, '');
        const pathSegments = pathname.split('/').filter(Boolean);
        const repoName = pathSegments[0] || `${owner}.github.io`;

        if (!owner || !repoName) {
            return null;
        }

        return {
            owner,
            name: repoName
        };
    },

    isLocalPreview: function() {
        if (typeof window === 'undefined' || !window.location) {
            return true;
        }

        const { hostname, protocol } = window.location;
        return protocol === 'file:'
            || hostname === ''
            || hostname === 'localhost'
            || hostname === '127.0.0.1'
            || hostname === '::1';
    },

    getLocalFallbackRepository: function() {
        if (!this.isLocalPreview()) {
            return null;
        }

        return {
            owner: this.fallbackRepoOwner,
            name: this.fallbackRepoName
        };
    },

    getRepository: function() {
        return this.getRuntimeRepository()
            || this.getConfiguredRepository()
            || this.getLocalFallbackRepository();
    },

    requireRepository: function() {
        const repository = this.getRepository();
        if (!repository) {
            throw new Error('Repository information is unavailable. Check data-config.js injection or the current Pages URL.');
        }

        return repository;
    },

    getRepoOwner: function() {
        return this.requireRepository().owner;
    },

    getRepoName: function() {
        return this.requireRepository().name;
    },

    getDataBranch: function() {
        return this.isPlaceholder(this.dataBranch) ? this.fallbackDataBranch : this.dataBranch;
    },

    getRepositoryUrl: function() {
        return `https://github.com/${this.getRepoOwner()}/${this.getRepoName()}`;
    },

    getRepositoryApiUrl: function() {
        return `https://api.github.com/repos/${this.getRepoOwner()}/${this.getRepoName()}`;
    },

    /**
     * Get the base URL for raw GitHub content from data branch
     * @returns {string} Base URL for raw GitHub content
     */
    getDataBaseUrl: function() {
        return `https://raw.githubusercontent.com/${this.getRepoOwner()}/${this.getRepoName()}/${this.getDataBranch()}`;
    },

    /**
     * Get the full URL for a data file
     * @param {string} filePath - Relative path to the data file (e.g., 'data/2025-01-01.jsonl')
     * @returns {string} Full URL to the data file
     */
    getDataUrl: function(filePath) {
        return `${this.getDataBaseUrl()}/${filePath}`;
    },

    applyRepositoryLinks: function() {
        if (typeof document === 'undefined') {
            return;
        }

        const repository = this.getRepository();
        if (!repository) {
            return;
        }

        const repoUrl = this.getRepositoryUrl();
        document.querySelectorAll('[data-github-link]').forEach((link) => {
            link.href = repoUrl;
        });
    }
};

if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        DATA_CONFIG.applyRepositoryLinks();
    });
}
