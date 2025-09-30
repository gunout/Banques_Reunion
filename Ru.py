import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class ReunionBankFinanceAnalyzer:
    def __init__(self, bank_name):
        self.bank = bank_name
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#F9A602', '#6A0572', 
                      '#AB83A1', '#5CAB7D', '#2A9D8F', '#E76F51', '#264653']
        
        self.start_year = 2002
        self.end_year = 2025
        
        # Configuration spécifique à chaque banque réunionnaise
        self.config = self._get_bank_config()
        
    def _get_bank_config(self):
        """Retourne la configuration spécifique pour chaque banque réunionnaise"""
        configs = {
            "Crédit Agricole de la Réunion": {
                "assets_base": 8500,
                "revenue_base": 450,
                "type": "cooperative",
                "specialites": ["agriculture", "pmie", "particuliers", "immobilier"],
                "marche": ["local", "regional"]
            },
            "Banque de la Réunion": {
                "assets_base": 4200,
                "revenue_base": 280,
                "type": "commerciale",
                "specialites": ["entreprises", "professionnels", "credit_bail"],
                "marche": ["local", "dom"]
            },
            "Société Générale Réunion": {
                "assets_base": 6800,
                "revenue_base": 380,
                "type": "commerciale",
                "specialites": ["grands_comptes", "banque_privee", "international"],
                "marche": ["local", "national", "international"]
            },
            "BNP Paribas Réunion": {
                "assets_base": 7200,
                "revenue_base": 410,
                "type": "commerciale",
                "specialites": ["corporates", "banque_investissement", "marches"],
                "marche": ["local", "national", "international"]
            },
            "Caisse d'Epargne Réunion": {
                "assets_base": 3500,
                "revenue_base": 220,
                "type": "mutualiste",
                "specialites": ["epargne", "habitat", "social"],
                "marche": ["local", "regional"]
            },
            "Banque Française Commerciale Océan Indien": {
                "assets_base": 2800,
                "revenue_base": 180,
                "type": "commerciale",
                "specialites": ["commerce", "tourisme", "professions_liberales"],
                "marche": ["regional", "ocean_indien"]
            },
            # Configuration par défaut pour les autres banques
            "default": {
                "assets_base": 1500,
                "revenue_base": 120,
                "type": "commerciale",
                "specialites": ["particuliers", "petites_entreprises"],
                "marche": ["local"]
            }
        }
        
        return configs.get(self.bank, configs["default"])
    
    def generate_financial_data(self):
        """Génère des données financières pour la banque"""
        print(f"🏦 Génération des données financières pour {self.bank}...")
        
        # Créer une base de données annuelle
        dates = pd.date_range(start=f'{self.start_year}-01-01', 
                             end=f'{self.end_year}-12-31', freq='Y')
        
        data = {'Annee': [date.year for date in dates]}
        
        # Données de base de la banque
        data['Total_Actifs'] = self._simulate_total_assets(dates)
        data['Fonds_Propres'] = self._simulate_equity(dates)
        data['Depots_Clients'] = self._simulate_customer_deposits(dates)
        data['Credits_Clients'] = self._simulate_customer_loans(dates)
        
        # Compte de résultat
        data['Produit_Net_Bancaire'] = self._simulate_net_banking_income(dates)
        data['Resultat_Net'] = self._simulate_net_income(dates)
        data['Charges_Exploitation'] = self._simulate_operating_costs(dates)
        data['Dotations_Provisions'] = self._simulate_provisions(dates)
        data['Impots'] = self._simulate_taxes(dates)
        
        # Indicateurs de rentabilité
        data['ROE'] = self._simulate_roe(dates)
        data['ROA'] = self._simulate_roa(dates)
        data['Marge_Interet'] = self._simulate_interest_margin(dates)
        data['Cout_Risque'] = self._simulate_cost_of_risk(dates)
        
        # Indicateurs de solidité
        data['Ratio_CET1'] = self._simulate_cet1_ratio(dates)
        data['Ratio_Liquidite'] = self._simulate_liquidity_ratio(dates)
        data['Ratio_Solvabilite'] = self._simulate_solvency_ratio(dates)
        data['Creances_Douteuses'] = self._simulate_npl(dates)
        
        # Répartition du crédit par secteur (spécifique à la Réunion)
        data['Credits_Particuliers'] = self._simulate_retail_loans(dates)
        data['Credits_Entreprises'] = self._simulate_corporate_loans(dates)
        data['Credits_Immobilier'] = self._simulate_real_estate_loans(dates)
        data['Credits_Agriculture'] = self._simulate_agriculture_loans(dates)
        data['Credits_Tourisme'] = self._simulate_tourism_loans(dates)
        data['Credits_Commerce'] = self._simulate_commerce_loans(dates)
        data['Credits_EC'] = self._simulate_energy_climate_loans(dates)
        
        df = pd.DataFrame(data)
        
        # Ajouter des tendances spécifiques au secteur bancaire réunionnais
        self._add_banking_trends(df)
        
        return df
    
    def _simulate_total_assets(self, dates):
        """Simule le total des actifs de la banque"""
        base_assets = self.config["assets_base"]
        
        assets = []
        for i, date in enumerate(dates):
            # Croissance variable selon le type de banque
            if self.config["type"] == "cooperative":
                growth_rate = 0.065  # Croissance forte pour les banques coopératives
            elif self.config["type"] == "mutualiste":
                growth_rate = 0.055
            else:
                growth_rate = 0.048  # Croissance pour les banques commerciales
                
            growth = 1 + growth_rate * i
            noise = np.random.normal(1, 0.06)
            assets.append(base_assets * growth * noise)
        
        return assets
    
    def _simulate_equity(self, dates):
        """Simule les fonds propres"""
        base_equity = self.config["assets_base"] * 0.085  # Ratio fonds propres/actifs
        
        equity = []
        for i, date in enumerate(dates):
            growth = 1 + 0.052 * i
            noise = np.random.normal(1, 0.05)
            equity.append(base_equity * growth * noise)
        
        return equity
    
    def _simulate_customer_deposits(self, dates):
        """Simule les dépôts clients"""
        base_deposits = self.config["assets_base"] * 0.65  # Part des dépôts dans les ressources
        
        deposits = []
        for i, date in enumerate(dates):
            growth = 1 + 0.045 * i
            noise = np.random.normal(1, 0.04)
            deposits.append(base_deposits * growth * noise)
        
        return deposits
    
    def _simulate_customer_loans(self, dates):
        """Simule les crédits clients"""
        base_loans = self.config["assets_base"] * 0.58  # Part des crédits dans les emplois
        
        loans = []
        for i, date in enumerate(dates):
            growth = 1 + 0.055 * i
            noise = np.random.normal(1, 0.07)
            loans.append(base_loans * growth * noise)
        
        return loans
    
    def _simulate_net_banking_income(self, dates):
        """Simule le produit net bancaire"""
        base_pnb = self.config["revenue_base"]
        
        pnb = []
        for i, date in enumerate(dates):
            if self.config["type"] == "cooperative":
                growth_rate = 0.058
            elif self.config["type"] == "mutualiste":
                growth_rate = 0.052
            else:
                growth_rate = 0.048
                
            growth = 1 + growth_rate * i
            noise = np.random.normal(1, 0.08)
            pnb.append(base_pnb * growth * noise)
        
        return pnb
    
    def _simulate_net_income(self, dates):
        """Simule le résultat net"""
        base_income = self.config["revenue_base"] * 0.22  # Marge nette
        
        income = []
        for i, date in enumerate(dates):
            year = date.year
            # Impact des crises sur la rentabilité
            if year in [2008, 2009, 2020, 2021]:
                crisis_multiplier = 0.75
            else:
                crisis_multiplier = 1.0
                
            growth = 1 + 0.045 * i
            noise = np.random.normal(1, 0.12)
            income.append(base_income * growth * crisis_multiplier * noise)
        
        return income
    
    def _simulate_operating_costs(self, dates):
        """Simule les charges d'exploitation"""
        base_costs = self.config["revenue_base"] * 0.62  # Ratio de charge
        
        costs = []
        for i, date in enumerate(dates):
            growth = 1 + 0.042 * i
            noise = np.random.normal(1, 0.05)
            costs.append(base_costs * growth * noise)
        
        return costs
    
    def _simulate_provisions(self, dates):
        """Simule les dotations aux provisions"""
        base_provisions = self.config["revenue_base"] * 0.08
        
        provisions = []
        for i, date in enumerate(dates):
            year = date.year
            # Augmentation des provisions en période de crise
            if year in [2008, 2009, 2020, 2021]:
                crisis_multiplier = 1.8
            else:
                crisis_multiplier = 1.0
                
            growth = 1 + 0.035 * i
            noise = np.random.normal(1, 0.20)
            provisions.append(base_provisions * growth * crisis_multiplier * noise)
        
        return provisions
    
    def _simulate_taxes(self, dates):
        """Simule les impôts"""
        base_taxes = self.config["revenue_base"] * 0.05
        
        taxes = []
        for i, date in enumerate(dates):
            year = date.year
            # Évolutions fiscales
            if year >= 2018:
                tax_rate = 1.15  # Hausse de la fiscalité
            else:
                tax_rate = 1.0
                
            growth = 1 + 0.04 * i
            noise = np.random.normal(1, 0.10)
            taxes.append(base_taxes * growth * tax_rate * noise)
        
        return taxes
    
    def _simulate_roe(self, dates):
        """Simule le Return on Equity"""
        roe_values = []
        for i, date in enumerate(dates):
            base_roe = 0.125  # ROE de base
            
            year = date.year
            if year in [2008, 2009, 2020, 2021]:
                crisis_impact = 0.65  # Baisse forte en crise
            else:
                crisis_impact = 1.0
            
            improvement = 1 + 0.002 * i  # Amélioration lente
            noise = np.random.normal(1, 0.08)
            roe_values.append(base_roe * crisis_impact * improvement * noise)
        
        return roe_values
    
    def _simulate_roa(self, dates):
        """Simule le Return on Assets"""
        roa_values = []
        for i, date in enumerate(dates):
            base_roa = 0.0085  # ROA de base
            
            year = date.year
            if year in [2008, 2009, 2020, 2021]:
                crisis_impact = 0.60
            else:
                crisis_impact = 1.0
            
            improvement = 1 + 0.0015 * i
            noise = np.random.normal(1, 0.07)
            roa_values.append(base_roa * crisis_impact * improvement * noise)
        
        return roa_values
    
    def _simulate_interest_margin(self, dates):
        """Simule la marge d'intérêt nette"""
        margins = []
        for i, date in enumerate(dates):
            base_margin = 0.018  # Marge de base
            
            year = date.year
            if year >= 2015:
                compression = 0.92  # Compression des marges due aux taux bas
            else:
                compression = 1.0
            
            noise = np.random.normal(1, 0.05)
            margins.append(base_margin * compression * noise)
        
        return margins
    
    def _simulate_cost_of_risk(self, dates):
        """Simule le coût du risque"""
        costs = []
        for i, date in enumerate(dates):
            base_cost = 0.0040  # Coût de base
            
            year = date.year
            if year in [2008, 2009, 2020, 2021]:
                crisis_multiplier = 2.5  # Forte hausse en crise
            else:
                crisis_multiplier = 1.0
            
            noise = np.random.normal(1, 0.15)
            costs.append(base_cost * crisis_multiplier * noise)
        
        return costs
    
    def _simulate_cet1_ratio(self, dates):
        """Simule le ratio CET1"""
        ratios = []
        for i, date in enumerate(dates):
            base_ratio = 0.125  # Ratio de base
            
            year = date.year
            if year >= 2014:
                regulatory_impact = 1.12  # Renforcement réglementaire
            else:
                regulatory_impact = 1.0
            
            improvement = 1 + 0.008 * i
            noise = np.random.normal(1, 0.04)
            ratios.append(base_ratio * regulatory_impact * improvement * noise)
        
        return ratios
    
    def _simulate_liquidity_ratio(self, dates):
        """Simule le ratio de liquidité"""
        ratios = []
        for i, date in enumerate(dates):
            base_ratio = 1.15  # Ratio LCR de base
            
            year = date.year
            if year >= 2015:
                regulatory_impact = 1.08  # Renforcement Bâle III
            else:
                regulatory_impact = 1.0
            
            noise = np.random.normal(1, 0.03)
            ratios.append(base_ratio * regulatory_impact * noise)
        
        return ratios
    
    def _simulate_solvency_ratio(self, dates):
        """Simule le ratio de solvabilité"""
        ratios = []
        for i, date in enumerate(dates):
            base_ratio = 0.145  # Ratio de base
            
            year = date.year
            if year >= 2014:
                regulatory_impact = 1.10
            else:
                regulatory_impact = 1.0
            
            improvement = 1 + 0.006 * i
            noise = np.random.normal(1, 0.04)
            ratios.append(base_ratio * regulatory_impact * improvement * noise)
        
        return ratios
    
    def _simulate_npl(self, dates):
        """Simule les créances douteuses"""
        npl_values = []
        for i, date in enumerate(dates):
            base_npl = 0.032  # Taux de base
            
            year = date.year
            if year in [2008, 2009, 2020, 2021]:
                crisis_multiplier = 1.9  # Forte hausse en crise
            else:
                crisis_multiplier = 1.0
            
            improvement = 1 - 0.005 * i  # Amélioration progressive
            noise = np.random.normal(1, 0.12)
            npl_values.append(base_npl * crisis_multiplier * improvement * noise)
        
        return npl_values
    
    def _simulate_retail_loans(self, dates):
        """Simule les crédits aux particuliers"""
        base_loans = self.config["assets_base"] * 0.25
        
        # Ajustement selon les spécialités
        multiplier = 1.4 if "particuliers" in self.config["specialites"] else 0.8
        
        loans = []
        for i, date in enumerate(dates):
            growth = 1 + 0.05 * i
            noise = np.random.normal(1, 0.08)
            loans.append(base_loans * growth * multiplier * noise)
        
        return loans
    
    def _simulate_corporate_loans(self, dates):
        """Simule les crédits aux entreprises"""
        base_loans = self.config["assets_base"] * 0.20
        
        multiplier = 1.5 if "entreprises" in self.config["specialites"] else 0.9
        
        loans = []
        for i, date in enumerate(dates):
            growth = 1 + 0.048 * i
            noise = np.random.normal(1, 0.10)
            loans.append(base_loans * growth * multiplier * noise)
        
        return loans
    
    def _simulate_real_estate_loans(self, dates):
        """Simule les crédits immobiliers"""
        base_loans = self.config["assets_base"] * 0.18
        
        multiplier = 1.6 if "immobilier" in self.config["specialites"] else 0.85
        
        loans = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2008, 2009]:
                crisis_multiplier = 0.7  # Crise immobilière
            else:
                crisis_multiplier = 1.0
                
            growth = 1 + 0.052 * i
            noise = np.random.normal(1, 0.09)
            loans.append(base_loans * growth * crisis_multiplier * multiplier * noise)
        
        return loans
    
    def _simulate_agriculture_loans(self, dates):
        """Simule les crédits agriculture (spécifique Réunion)"""
        base_loans = self.config["assets_base"] * 0.06
        
        multiplier = 2.0 if "agriculture" in self.config["specialites"] else 0.7
        
        loans = []
        for i, date in enumerate(dates):
            growth = 1 + 0.04 * i
            noise = np.random.normal(1, 0.11)
            loans.append(base_loans * growth * multiplier * noise)
        
        return loans
    
    def _simulate_tourism_loans(self, dates):
        """Simule les crédits tourisme (spécifique Réunion)"""
        base_loans = self.config["assets_base"] * 0.05
        
        multiplier = 1.8 if "tourisme" in self.config["specialites"] else 0.8
        
        loans = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2020, 2021]:
                crisis_multiplier = 0.6  # Fort impact COVID sur tourisme
            else:
                crisis_multiplier = 1.0
                
            growth = 1 + 0.046 * i
            noise = np.random.normal(1, 0.13)
            loans.append(base_loans * growth * crisis_multiplier * multiplier * noise)
        
        return loans
    
    def _simulate_commerce_loans(self, dates):
        """Simule les crédits commerce (spécifique Réunion)"""
        base_loans = self.config["assets_base"] * 0.04
        
        multiplier = 1.7 if "commerce" in self.config["specialites"] else 0.9
        
        loans = []
        for i, date in enumerate(dates):
            growth = 1 + 0.044 * i
            noise = np.random.normal(1, 0.10)
            loans.append(base_loans * growth * multiplier * noise)
        
        return loans
    
    def _simulate_energy_climate_loans(self, dates):
        """Simule les crédits énergie-climat (spécifique Réunion)"""
        base_loans = self.config["assets_base"] * 0.03
        
        loans = []
        for i, date in enumerate(dates):
            year = date.year
            if year >= 2015:
                growth_accelerator = 1 + 0.08 * (year - 2015)  # Croissance forte
            else:
                growth_accelerator = 1.0
                
            noise = np.random.normal(1, 0.14)
            loans.append(base_loans * growth_accelerator * noise)
        
        return loans
    
    def _add_banking_trends(self, df):
        """Ajoute des tendances bancaires réalistes adaptées à la Réunion"""
        for i, row in df.iterrows():
            year = row['Annee']
            
            # Croissance économique de la Réunion (2002-2007)
            if 2002 <= year <= 2007:
                df.loc[i, 'Credits_Clients'] *= 1.08
                df.loc[i, 'Resultat_Net'] *= 1.06
            
            # Crise financière mondiale (2008-2009)
            if 2008 <= year <= 2009:
                df.loc[i, 'Resultat_Net'] *= 0.72
                df.loc[i, 'Dotations_Provisions'] *= 1.85
                df.loc[i, 'Creances_Douteuses'] *= 1.45
            
            # reprise post-crise (2010-2014)
            elif 2010 <= year <= 2014:
                df.loc[i, 'Credits_Clients'] *= 1.05
                df.loc[i, 'ROE'] *= 1.08
            
            # Bâle III et réglementation renforcée (2014-2018)
            if 2014 <= year <= 2018:
                df.loc[i, 'Ratio_CET1'] *= 1.12
                df.loc[i, 'Ratio_Liquidite'] *= 1.06
            
            # Développement durable et énergies renouvelables (2015+)
            if year >= 2015:
                df.loc[i, 'Credits_EC'] *= 1.25
            
            # Crise COVID-19 (2020-2021)
            if 2020 <= year <= 2021:
                if year == 2020:
                    df.loc[i, 'Resultat_Net'] *= 0.68
                    df.loc[i, 'Dotations_Provisions'] *= 1.95
                    df.loc[i, 'Credits_Tourisme'] *= 0.55
            
            # Plan de relance et reprise post-COVID (2022-2025)
            if year >= 2022:
                df.loc[i, 'Credits_Entreprises'] *= 1.12
                df.loc[i, 'Credits_EC'] *= 1.35
                df.loc[i, 'Resultat_Net'] *= 1.08
    
    def create_financial_analysis(self, df):
        """Crée une analyse complète des finances de la banque"""
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 24))
        
        # 1. Évolution des actifs et crédits
        ax1 = plt.subplot(4, 2, 1)
        self._plot_assets_loans(df, ax1)
        
        # 2. Compte de résultat
        ax2 = plt.subplot(4, 2, 2)
        self._plot_income_statement(df, ax2)
        
        # 3. Rentabilité
        ax3 = plt.subplot(4, 2, 3)
        self._plot_profitability(df, ax3)
        
        # 4. Répartition des crédits
        ax4 = plt.subplot(4, 2, 4)
        self._plot_loan_distribution(df, ax4)
        
        # 5. Solidité financière
        ax5 = plt.subplot(4, 2, 5)
        self._plot_financial_strength(df, ax5)
        
        # 6. Risques
        ax6 = plt.subplot(4, 2, 6)
        self._plot_risk_indicators(df, ax6)
        
        # 7. Dépôts et ressources
        ax7 = plt.subplot(4, 2, 7)
        self._plot_deposits_resources(df, ax7)
        
        # 8. Performance opérationnelle
        ax8 = plt.subplot(4, 2, 8)
        self._plot_operational_performance(df, ax8)
        
        plt.suptitle(f'Analyse Financière de {self.bank} - Île de la Réunion ({self.start_year}-{self.end_year})', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.bank.replace(" ", "_")}_financial_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Générer les insights
        self._generate_financial_insights(df)
    
    def _plot_assets_loans(self, df, ax):
        """Plot de l'évolution des actifs et crédits"""
        ax.plot(df['Annee'], df['Total_Actifs'], label='Total Actifs', 
               linewidth=2, color='#2A9D8F', alpha=0.8)
        ax.plot(df['Annee'], df['Credits_Clients'], label='Crédits Clients', 
               linewidth=2, color='#E76F51', alpha=0.8)
        ax.plot(df['Annee'], df['Fonds_Propres'], label='Fonds Propres', 
               linewidth=2, color='#264653', alpha=0.8)
        
        ax.set_title('Évolution des Actifs et Crédits (M€)', 
                    fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_income_statement(self, df, ax):
        """Plot du compte de résultat"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Produit_Net_Bancaire', 'Charges_Exploitation', 
                     'Dotations_Provisions', 'Impots', 'Resultat_Net']
        colors = ['#2A9D8F', '#E76F51', '#F9A602', '#6A0572', '#264653']
        labels = ['PNB', 'Charges Exploitation', 'Provisions', 'Impôts', 'Résultat Net']
        
        for i, category in enumerate(categories):
            if category == 'Resultat_Net':
                # Le résultat net est affiché séparément en ligne
                ax.plot(years, df[category], label=labels[i], 
                       linewidth=3, color=colors[i], marker='o')
            else:
                ax.bar(years, df[category], width, label=labels[i], 
                      bottom=bottom, color=colors[i], alpha=0.8)
                bottom += df[category]
        
        ax.set_title('Compte de Résultat (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_profitability(self, df, ax):
        """Plot des indicateurs de rentabilité"""
        # ROE
        ax.plot(df['Annee'], df['ROE'], label='ROE (%)', 
               linewidth=2, color='#2A9D8F', alpha=0.8)
        
        ax.set_title('Rentabilité', fontsize=12, fontweight='bold')
        ax.set_ylabel('ROE (%)', color='#2A9D8F')
        ax.tick_params(axis='y', labelcolor='#2A9D8F')
        ax.grid(True, alpha=0.3)
        
        # ROA en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['ROA'], label='ROA (%)', 
                linewidth=2, color='#E76F51', alpha=0.8)
        ax2.set_ylabel('ROA (%)', color='#E76F51')
        ax2.tick_params(axis='y', labelcolor='#E76F51')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_loan_distribution(self, df, ax):
        """Plot de la répartition des crédits"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Credits_Particuliers', 'Credits_Entreprises', 
                     'Credits_Immobilier', 'Credits_Agriculture',
                     'Credits_Tourisme', 'Credits_Commerce', 'Credits_EC']
        colors = ['#264653', '#2A9D8F', '#E76F51', '#F9A602', 
                 '#6A0572', '#45B7D1', '#5CAB7D']
        labels = ['Particuliers', 'Entreprises', 'Immobilier', 'Agriculture',
                 'Tourisme', 'Commerce', 'Énergie-Climat']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title('Répartition des Crédits par Secteur (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_financial_strength(self, df, ax):
        """Plot des indicateurs de solidité financière"""
        # Ratio CET1
        ax.plot(df['Annee'], df['Ratio_CET1'], label='Ratio CET1', 
               linewidth=2, color='#264653', alpha=0.8)
        
        ax.set_title('Solidité Financière', fontsize=12, fontweight='bold')
        ax.set_ylabel('Ratio CET1', color='#264653')
        ax.tick_params(axis='y', labelcolor='#264653')
        ax.grid(True, alpha=0.3)
        
        # Ratio de solvabilité en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Ratio_Solvabilite'], label='Ratio Solvabilité', 
                linewidth=2, color='#E76F51', alpha=0.8)
        ax2.set_ylabel('Ratio Solvabilité', color='#E76F51')
        ax2.tick_params(axis='y', labelcolor='#E76F51')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_risk_indicators(self, df, ax):
        """Plot des indicateurs de risque"""
        # Créances douteuses
        ax.bar(df['Annee'], df['Creances_Douteuses'], label='Créances Douteuses (%)', 
              color='#E76F51', alpha=0.7)
        
        ax.set_title('Indicateurs de Risque', fontsize=12, fontweight='bold')
        ax.set_ylabel('Créances Douteuses (%)', color='#E76F51')
        ax.tick_params(axis='y', labelcolor='#E76F51')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Coût du risque en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Cout_Risque'], label='Coût du Risque (%)', 
                linewidth=3, color='#264653')
        ax2.set_ylabel('Coût du Risque (%)', color='#264653')
        ax2.tick_params(axis='y', labelcolor='#264653')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_deposits_resources(self, df, ax):
        """Plot des dépôts et ressources"""
        ax.plot(df['Annee'], df['Depots_Clients'], label='Dépôts Clients', 
               linewidth=2, color='#2A9D8F', alpha=0.8)
        ax.plot(df['Annee'], df['Credits_Clients'], label='Crédits Clients', 
               linewidth=2, color='#E76F51', alpha=0.8)
        
        ax.set_title('Dépôts vs Crédits (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_operational_performance(self, df, ax):
        """Plot de la performance opérationnelle"""
        # Marge d'intérêt
        ax.plot(df['Annee'], df['Marge_Interet'], label='Marge d\'Intérêt Nette (%)', 
               linewidth=2, color='#264653', alpha=0.8)
        
        ax.set_title('Performance Opérationnelle', fontsize=12, fontweight='bold')
        ax.set_ylabel('Marge d\'Intérêt (%)', color='#264653')
        ax.tick_params(axis='y', labelcolor='#264653')
        ax.grid(True, alpha=0.3)
        
        # Ratio de liquidité en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Ratio_Liquidite'], label='Ratio Liquidité', 
                linewidth=2, color='#F9A602', alpha=0.8)
        ax2.set_ylabel('Ratio Liquidité', color='#F9A602')
        ax2.tick_params(axis='y', labelcolor='#F9A602')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _generate_financial_insights(self, df):
        """Génère des insights analytiques adaptés au secteur bancaire réunionnais"""
        print(f"🏦 INSIGHTS ANALYTIQUES - {self.bank} (Île de la Réunion)")
        print("=" * 60)
        
        # 1. Statistiques de base
        print("\n1. 📈 STATISTIQUES GÉNÉRALES:")
        avg_assets = df['Total_Actifs'].mean()
        avg_loans = df['Credits_Clients'].mean()
        avg_income = df['Resultat_Net'].mean()
        avg_roe = df['ROE'].mean() * 100
        
        print(f"Actifs moyens annuels: {avg_assets:.0f} M€")
        print(f"Crédits clients moyens: {avg_loans:.0f} M€")
        print(f"Résultat net moyen: {avg_income:.1f} M€")
        print(f"ROE moyen: {avg_roe:.1f}%")
        
        # 2. Croissance
        print("\n2. 📊 TAUX DE CROISSANCE:")
        assets_growth = ((df['Total_Actifs'].iloc[-1] / 
                         df['Total_Actifs'].iloc[0]) - 1) * 100
        income_growth = ((df['Resultat_Net'].iloc[-1] / 
                         df['Resultat_Net'].iloc[0]) - 1) * 100
        
        print(f"Croissance des actifs ({self.start_year}-{self.end_year}): {assets_growth:.1f}%")
        print(f"Croissance du résultat net ({self.start_year}-{self.end_year}): {income_growth:.1f}%")
        
        # 3. Structure financière
        print("\n3. 📋 STRUCTURE FINANCIÈRE:")
        loans_assets_ratio = (df['Credits_Clients'].mean() / df['Total_Actifs'].mean()) * 100
        deposits_loans_ratio = (df['Depots_Clients'].mean() / df['Credits_Clients'].mean()) * 100
        equity_ratio = (df['Fonds_Propres'].mean() / df['Total_Actifs'].mean()) * 100
        
        print(f"Ratio crédits/actifs: {loans_assets_ratio:.1f}%")
        print(f"Ratio dépôts/crédits: {deposits_loans_ratio:.1f}%")
        print(f"Ratio fonds propres: {equity_ratio:.1f}%")
        
        # 4. Rentabilité et risque
        print("\n4. 💰 RENTABILITÉ ET RISQUE:")
        avg_roa = df['ROA'].mean() * 100
        avg_cost_risk = df['Cout_Risque'].mean() * 100
        avg_npl = df['Creances_Douteuses'].mean() * 100
        last_cet1 = df['Ratio_CET1'].iloc[-1] * 100
        
        print(f"ROA moyen: {avg_roa:.2f}%")
        print(f"Coût du risque moyen: {avg_cost_risk:.2f}%")
        print(f"Créances douteuses moyennes: {avg_npl:.2f}%")
        print(f"Ratio CET1 final: {last_cet1:.1f}%")
        
        # 5. Spécificités de la banque réunionnaise
        print(f"\n5. 🌟 SPÉCIFICITÉS DE {self.bank.upper()} (RÉUNION):")
        print(f"Type de banque: {self.config['type']}")
        print(f"Spécialités: {', '.join(self.config['specialites'])}")
        print(f"Marchés: {', '.join(self.config['marche'])}")
        
        # 6. Événements marquants spécifiques à la Réunion
        print("\n6. 📅 ÉVÉNEMENTS MARQUANTS RÉUNION:")
        print("• 2002-2007: Croissance économique forte de la Réunion")
        print("• 2008-2009: Crise financière mondiale (impact modéré)")
        print("• 2010-2014: Reprise et développement des infrastructures")
        print("• 2014-2018: Mise en œuvre Bâle III et réglementation renforcée")
        print("• 2015+: Développement des financements énergies renouvelables")
        print("• 2020-2021: Crise COVID-19 (fort impact tourisme)")
        print("• 2022-2025: Plan de relance et transition énergétique")
        
        # 7. Recommandations stratégiques adaptées à la Réunion
        print("\n7. 💡 RECOMMANDATIONS STRATÉGIQUES:")
        if "agriculture" in self.config["specialites"]:
            print("• Développer les financements agriculture durable et bio")
            print("• Soutenir la transformation des productions locales")
        if "tourisme" in self.config["specialites"]:
            print("• Accompagner la reprise et transformation du secteur touristique")
            print("• Financer l'écotourisme et l'hébergement durable")
        if "pmie" in self.config["specialites"]:
            print("• Renforcer le soutien aux PME/TPE réunionnaises")
            print("• Développer le digital banking pour les entreprises")
        
        print("• Accélérer les financements transition énergétique (solaire, biomasse)")
        print("• Développer les produits d'épargne durable et responsable")
        print("• Renforcer la bancarisation dans les zones rurales")
        print("• Investir dans la digitalisation et l'innovation financière")
        print("• Développer les partenariats avec les acteurs locaux")

def main():
    """Fonction principale pour la Réunion"""
    # Liste des banques de la Réunion
    banques = [
        "Crédit Agricole de la Réunion",
        "Banque de la Réunion", 
        "Société Générale Réunion",
        "BNP Paribas Réunion",
        "Caisse d'Epargne Réunion",
        "Banque Française Commerciale Océan Indien"
    ]
    
    print("🏦 ANALYSE DES BANQUES DE L'ÎLE DE LA RÉUNION (2002-2025)")
    print("=" * 60)
    
    # Demander à l'utilisateur de choisir une banque
    print("Liste des banques disponibles:")
    for i, banque in enumerate(banques, 1):
        print(f"{i}. {banque}")
    
    try:
        choix = int(input("\nChoisissez le numéro de la banque à analyser: "))
        if choix < 1 or choix > len(banques):
            raise ValueError
        banque_selectionnee = banques[choix-1]
    except (ValueError, IndexError):
        print("Choix invalide. Sélection du Crédit Agricole par défaut.")
        banque_selectionnee = "Crédit Agricole de la Réunion"
    
    # Initialiser l'analyseur
    analyzer = ReunionBankFinanceAnalyzer(banque_selectionnee)
    
    # Générer les données
    financial_data = analyzer.generate_financial_data()
    
    # Sauvegarder les données
    output_file = f'{banque_selectionnee.replace(" ", "_")}_financial_data_2002_2025.csv'
    financial_data.to_csv(output_file, index=False)
    print(f"💾 Données sauvegardées: {output_file}")
    
    # Aperçu des données
    print("\n👀 Aperçu des données:")
    print(financial_data[['Annee', 'Total_Actifs', 'Produit_Net_Bancaire', 'Resultat_Net', 'ROE']].head())
    
    # Créer l'analyse
    print("\n📈 Création de l'analyse financière...")
    analyzer.create_financial_analysis(financial_data)
    
    print(f"\n✅ Analyse financière de {banque_selectionnee} terminée!")
    print(f"📊 Période: {analyzer.start_year}-{analyzer.end_year}")
    print("📦 Données: Actifs, rentabilité, risques, crédits par secteur")

if __name__ == "__main__":
    main()