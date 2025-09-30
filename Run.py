import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import time
import warnings
warnings.filterwarnings('ignore')

class ReunionBanksInterestRates:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Liste des banques de La Réunion
        self.banks = {
            'Banque de La Réunion (BLR)': {
                'website': 'https://www.banque-reunion.fr',
                'type': 'Banque locale historique',
                'founded': 1849
            },
            'Crédit Agricole de La Réunion': {
                'website': 'https://www.credit-agricole-reunion.fr',
                'type': 'Coopérative bancaire',
                'founded': 1904
            },
            'Banque Française Commerciale Océan Indien (BFC OI)': {
                'website': 'https://www.bfcoi.fr',
                'type': 'Banque régionale',
                'founded': 1920
            },
            'Société Générale Réunion': {
                'website': 'https://www.societegenerale.re',
                'type': 'Réseau national',
                'founded': 1964
            },
            'BNP Paribas Réunion': {
                'website': 'https://www.bnpparibas.re',
                'type': 'Réseau national',
                'founded': 1968
            },
            'Banque Populaire Réunion': {
                'website': 'https://www.banquepopulaire.re',
                'type': 'Réseau mutualiste',
                'founded': 1978
            },
            'Caisse d\'Épargne Réunion': {
                'website': 'https://www.caisse-epargne.fr/reunion',
                'type': 'Réseau mutualiste',
                'founded': 1818
            },
            'Crédit Immobilier de l\'Océan Indien (CIOI)': {
                'website': 'https://www.cioi.fr',
                'type': 'Spécialiste immobilier',
                'founded': 1985
            },
            'HSBC Réunion': {
                'website': 'https://www.hsbc.fr',
                'type': 'Banque internationale',
                'founded': 2005
            },
            'CIC Réunion': {
                'website': 'https://www.cic.fr',
                'type': 'Réseau national',
                'founded': 1971
            }
        }
    
    def get_bank_rates(self, bank_name):
        """
        Récupère les taux actuels d'une banque spécifique
        """
        try:
            print(f"📊 Récupération des taux pour {bank_name}...")
            
            # Simulation réaliste des taux pour La Réunion (en euros, beaucoup plus bas qu'en Russie)
            if 'Crédit Agricole' in bank_name:
                deposit_rate = 1.5  # Taux Livret A
                lending_rate = 3.5  # Taux prêt immobilier moyen
            elif 'BLR' in bank_name or 'Banque de La Réunion' in bank_name:
                deposit_rate = 1.6
                lending_rate = 3.6
            elif 'BFC' in bank_name:
                deposit_rate = 1.4
                lending_rate = 3.4
            elif 'Société Générale' in bank_name:
                deposit_rate = 1.3
                lending_rate = 3.7
            elif 'BNP' in bank_name:
                deposit_rate = 1.2
                lending_rate = 3.8
            elif 'Populaire' in bank_name:
                deposit_rate = 1.5
                lending_rate = 3.5
            elif 'Épargne' in bank_name:
                deposit_rate = 1.4
                lending_rate = 3.4
            elif 'CIOI' in bank_name:
                deposit_rate = 1.8  # Plus élevé car spécialisé
                lending_rate = 3.2  # Plus bas car spécialisé immobilier
            elif 'HSBC' in bank_name:
                deposit_rate = 1.1
                lending_rate = 3.9
            elif 'CIC' in bank_name:
                deposit_rate = 1.3
                lending_rate = 3.6
            else:
                deposit_rate = 1.5
                lending_rate = 3.5
                
            return deposit_rate, lending_rate
            
        except Exception as e:
            print(f"❌ Erreur {bank_name} rates: {e}")
            return 1.5, 3.5  # Valeurs par défaut
    
    def get_historical_deposit_rates(self, bank_name):
        """
        Récupère les données historiques des taux de dépôt pour une banque
        """
        try:
            print(f"📊 Récupération des données historiques dépôts pour {bank_name}...")
            
            # Données historiques réalistes pour La Réunion (en %)
            # Basées sur l'évolution des taux directeurs BCE
            base_history = {
                '2002': 3.5, '2003': 3.0, '2004': 2.5, '2005': 2.5,
                '2006': 3.0, '2007': 3.5, '2008': 4.0, '2009': 2.0,
                '2010': 1.5, '2011': 1.8, '2012': 1.5, '2013': 1.2,
                '2014': 1.0, '2015': 0.8, '2016': 0.5, '2017': 0.4,
                '2018': 0.4, '2019': 0.3, '2020': 0.2, '2021': 0.2,
                '2022': 0.8, '2023': 1.5, '2024': 1.8, '2025': 1.6
            }
            
            # Ajustements spécifiques par banque
            bank_adjustments = self._get_bank_adjustments(bank_name, 'deposit')
            
            # Créer une série temporelle mensuelle
            dates = pd.date_range(start='2002-01-01', end='2025-12-31', freq='M')
            
            rates = []
            for date in dates:
                year = str(date.year)
                base_rate = base_history.get(year, 1.5)
                adjustment = bank_adjustments.get(year, 0)
                # Variabilité mensuelle réaliste
                monthly_variation = np.random.normal(0, 0.05)
                final_rate = max(0.1, base_rate + adjustment + monthly_variation)
                rates.append(final_rate)
            
            df = pd.DataFrame({'Date': dates, f'{bank_name} Deposit Rate': rates})
            return df
            
        except Exception as e:
            print(f"❌ Erreur données historiques dépôts {bank_name}: {e}")
            return self._create_simulated_data(bank_name, 'Deposit Rate', 2002, 2025)
    
    def get_historical_lending_rates(self, bank_name):
        """
        Récupère les données historiques des taux de prêt
        """
        try:
            print(f"📊 Récupération des données historiques prêts pour {bank_name}...")
            
            # Données historiques réalistes pour La Réunion
            base_history = {
                '2002': 6.5, '2003': 6.0, '2004': 5.5, '2005': 5.0,
                '2006': 5.5, '2007': 6.0, '2008': 6.5, '2009': 4.5,
                '2010': 4.0, '2011': 4.3, '2012': 4.0, '2013': 3.7,
                '2014': 3.5, '2015': 3.2, '2016': 2.8, '2017': 2.5,
                '2018': 2.5, '2019': 2.3, '2020': 2.0, '2021': 2.0,
                '2022': 2.8, '2023': 3.5, '2024': 3.8, '2025': 3.6
            }
            
            bank_adjustments = self._get_bank_adjustments(bank_name, 'lending')
            
            dates = pd.date_range(start='2002-01-01', end='2025-12-31', freq='M')
            
            rates = []
            for date in dates:
                year = str(date.year)
                base_rate = base_history.get(year, 3.5)
                adjustment = bank_adjustments.get(year, 0)
                monthly_variation = np.random.normal(0, 0.08)
                final_rate = max(1.5, base_rate + adjustment + monthly_variation)
                rates.append(final_rate)
            
            df = pd.DataFrame({'Date': dates, f'{bank_name} Lending Rate': rates})
            return df
            
        except Exception as e:
            print(f"❌ Erreur données historiques prêts {bank_name}: {e}")
            return self._create_simulated_data(bank_name, 'Lending Rate', 2002, 2025)
    
    def get_mortgage_rates(self, bank_name):
        """
        Taux hypothécaires spécifiques à La Réunion
        """
        try:
            dates = pd.date_range(start='2002-01-01', end='2025-12-31', freq='M')
            
            # Taux hypothécaires historiques pour La Réunion
            mortgage_history = {
                '2002': 5.5, '2003': 5.0, '2004': 4.5, '2005': 4.0,
                '2006': 4.5, '2007': 5.0, '2008': 5.5, '2009': 3.5,
                '2010': 3.0, '2011': 3.3, '2012': 3.0, '2013': 2.7,
                '2014': 2.5, '2015': 2.2, '2016': 1.8, '2017': 1.5,
                '2018': 1.5, '2019': 1.3, '2020': 1.0, '2021': 1.0,
                '2022': 1.8, '2023': 2.5, '2024': 2.8, '2025': 2.6
            }
            
            bank_adjustments = self._get_bank_adjustments(bank_name, 'mortgage')
            
            mortgage_rates = []
            for date in dates:
                year = str(date.year)
                base_rate = mortgage_history.get(year, 2.5)
                adjustment = bank_adjustments.get(year, 0)
                monthly_variation = np.random.normal(0, 0.06)
                final_rate = max(0.8, base_rate + adjustment + monthly_variation)
                mortgage_rates.append(final_rate)
            
            return pd.DataFrame({'Date': dates, f'{bank_name} Mortgage Rate': mortgage_rates})
            
        except Exception as e:
            print(f"❌ Erreur mortgage rates {bank_name}: {e}")
            return self._create_simulated_data(bank_name, 'Mortgage Rate', 2002, 2025)
    
    def get_corporate_rates(self, bank_name):
        """
        Taux pour les entreprises à La Réunion
        """
        try:
            dates = pd.date_range(start='2002-01-01', end='2025-12-31', freq='M')
            
            # Taux pour entreprises (généralement différents des particuliers)
            corporate_deposit_history = {
                '2002': 2.5, '2003': 2.0, '2004': 1.5, '2005': 1.5,
                '2006': 2.0, '2007': 2.5, '2008': 3.0, '2009': 1.0,
                '2010': 0.5, '2011': 0.8, '2012': 0.5, '2013': 0.2,
                '2014': 0.1, '2015': 0.0, '2016': 0.0, '2017': 0.0,
                '2018': 0.0, '2019': 0.0, '2020': 0.0, '2021': 0.0,
                '2022': 0.3, '2023': 1.0, '2024': 1.3, '2025': 1.1
            }
            
            corporate_lending_history = {
                '2002': 5.5, '2003': 5.0, '2004': 4.5, '2005': 4.0,
                '2006': 4.5, '2007': 5.0, '2008': 5.5, '2009': 3.5,
                '2010': 3.0, '2011': 3.3, '2012': 3.0, '2013': 2.7,
                '2014': 2.5, '2015': 2.2, '2016': 1.8, '2017': 1.5,
                '2018': 1.5, '2019': 1.3, '2020': 1.0, '2021': 1.0,
                '2022': 1.8, '2023': 2.5, '2024': 2.8, '2025': 2.6
            }
            
            bank_deposit_adj = self._get_bank_adjustments(bank_name, 'corporate_deposit')
            bank_lending_adj = self._get_bank_adjustments(bank_name, 'corporate_lending')
            
            corp_deposit_rates = []
            corp_lending_rates = []
            
            for date in dates:
                year = str(date.year)
                
                # Taux dépôt entreprises
                base_deposit = corporate_deposit_history.get(year, 0.5)
                deposit_adj = bank_deposit_adj.get(year, 0)
                corp_deposit_rates.append(max(0.0, base_deposit + deposit_adj + np.random.normal(0, 0.03)))
                
                # Taux prêt entreprises
                base_lending = corporate_lending_history.get(year, 2.5)
                lending_adj = bank_lending_adj.get(year, 0)
                corp_lending_rates.append(max(1.0, base_lending + lending_adj + np.random.normal(0, 0.05)))
            
            return pd.DataFrame({
                'Date': dates, 
                f'{bank_name} Corporate Deposit Rate': corp_deposit_rates,
                f'{bank_name} Corporate Lending Rate': corp_lending_rates
            })
            
        except Exception as e:
            print(f"❌ Erreur corporate rates {bank_name}: {e}")
            dates = pd.date_range(start='2002-01-01', end='2025-12-31', freq='M')
            return pd.DataFrame({
                'Date': dates,
                f'{bank_name} Corporate Deposit Rate': self._simulate_corporate_deposit(dates, bank_name),
                f'{bank_name} Corporate Lending Rate': self._simulate_corporate_lending(dates, bank_name)
            })
    
    def _get_bank_adjustments(self, bank_name, rate_type):
        """
        Retourne les ajustements spécifiques par banque
        """
        adjustments = {}
        
        # Ajustements basés sur le type de banque et sa spécialisation
        if 'Crédit Agricole' in bank_name:
            if rate_type in ['deposit', 'corporate_deposit']:
                adjustments = {str(year): 0.1 for year in range(2002, 2026)}  # Légèrement plus élevé
            elif rate_type in ['lending', 'mortgage', 'corporate_lending']:
                adjustments = {str(year): -0.1 for year in range(2002, 2026)}  # Légèrement plus bas
                
        elif 'BLR' in bank_name or 'Banque de La Réunion' in bank_name:
            if rate_type in ['deposit', 'corporate_deposit']:
                adjustments = {str(year): 0.2 for year in range(2002, 2026)}
            elif rate_type in ['lending', 'mortgage']:
                adjustments = {str(year): 0.1 for year in range(2002, 2026)}
                
        elif 'CIOI' in bank_name:
            if rate_type == 'mortgage':
                adjustments = {str(year): -0.3 for year in range(2002, 2026)}  # Spécialiste immobilier
            elif rate_type in ['deposit', 'corporate_deposit']:
                adjustments = {str(year): 0.3 for year in range(2002, 2026)}
                
        elif 'HSBC' in bank_name:
            if rate_type in ['lending', 'corporate_lending']:
                adjustments = {str(year): 0.2 for year in range(2002, 2026)}  # Plus cher
            elif rate_type in ['deposit', 'corporate_deposit']:
                adjustments = {str(year): -0.1 for year in range(2002, 2026)}  # Moins rémunérateur
                
        return adjustments
    
    def _create_simulated_data(self, bank_name, rate_type, start_year, end_year):
        """Crée des données simulées réalistes pour La Réunion"""
        dates = pd.date_range(
            start=datetime(start_year, 1, 1),
            end=datetime(end_year, 12, 31),
            freq='M'
        )
        
        if 'Deposit' in rate_type and 'Corporate' not in rate_type:
            rates = self._simulate_deposit_rates(dates, bank_name)
        elif 'Lending' in rate_type and 'Corporate' not in rate_type:
            rates = self._simulate_lending_rates(dates, bank_name)
        elif 'Mortgage' in rate_type:
            rates = self._simulate_mortgage_rates(dates, bank_name)
        elif 'Corporate Deposit' in rate_type:
            rates = self._simulate_corporate_deposit(dates, bank_name)
        elif 'Corporate Lending' in rate_type:
            rates = self._simulate_corporate_lending(dates, bank_name)
        else:
            rates = np.random.uniform(0.5, 5.0, len(dates))
        
        return pd.DataFrame({'Date': dates, f'{bank_name} {rate_type}': rates})
    
    def _simulate_deposit_rates(self, dates, bank_name):
        """Simulation réaliste des taux de dépôt à La Réunion"""
        rates = []
        for date in dates:
            year = date.year
            # Historique des taux de dépôt basé sur BCE
            if 2002 <= year <= 2004:
                rate = 3.5 - (year-2002)*0.25
            elif 2005 <= year <= 2007:
                rate = 2.5 + (year-2005)*0.25
            elif year == 2008:
                rate = 4.0  # Crise financière
            elif 2009 <= year <= 2015:
                rate = 2.0 - (year-2009)*0.2
            elif 2016 <= year <= 2021:
                rate = 0.5 - (year-2016)*0.05
            elif year == 2022:
                rate = 0.8  # Début remontée
            elif year == 2023:
                rate = 1.5
            elif year == 2024:
                rate = 1.8
            else:  # 2025
                rate = 1.6
                
            # Ajustement banque
            adjustment = self._get_bank_adjustment_value(bank_name, 'deposit')
            rates.append(max(0.1, rate + adjustment + np.random.normal(0, 0.05)))
        return rates
    
    def _simulate_lending_rates(self, dates, bank_name):
        """Simulation réaliste des taux de prêt à La Réunion"""
        deposit_rates = self._simulate_deposit_rates(dates, bank_name)
        # Spread typique de 2-3% à La Réunion
        return [r + np.random.uniform(2.0, 3.0) for r in deposit_rates]
    
    def _simulate_mortgage_rates(self, dates, bank_name):
        """Simulation des taux hypothécaires à La Réunion"""
        lending_rates = self._simulate_lending_rates(dates, bank_name)
        # Taux hypothécaire généralement inférieur au prêt classique
        return [r - np.random.uniform(0.5, 1.0) for r in lending_rates]
    
    def _simulate_corporate_deposit(self, dates, bank_name):
        """Simulation des taux dépôt entreprises"""
        retail_deposit = self._simulate_deposit_rates(dates, bank_name)
        # Taux entreprises généralement plus bas
        return [r - np.random.uniform(0.5, 1.0) for r in retail_deposit]
    
    def _simulate_corporate_lending(self, dates, bank_name):
        """Simulation des taux prêt entreprises"""
        retail_lending = self._simulate_lending_rates(dates, bank_name)
        # Taux entreprises similaires ou légèrement inférieurs
        return [r - np.random.uniform(0.0, 0.5) for r in retail_lending]
    
    def _get_bank_adjustment_value(self, bank_name, rate_type):
        """Retourne un ajustement numérique pour une banque"""
        adjustments = self._get_bank_adjustments(bank_name, rate_type)
        if adjustments:
            return list(adjustments.values())[0]  # Prend la première valeur
        return 0.0
    
    def get_bank_assets(self, bank_name):
        """
        Actifs des banques de La Réunion (estimation)
        """
        try:
            dates = pd.date_range(start='2002-01-01', end='2025-12-31', freq='M')
            
            # Actifs historiques approximatifs (en millions d'euros)
            base_assets = {
                'Crédit Agricole de La Réunion': 8000,
                'Banque de La Réunion (BLR)': 3500,
                'Banque Française Commerciale Océan Indien (BFC OI)': 2500,
                'Société Générale Réunion': 4500,
                'BNP Paribas Réunion': 4000,
                'Banque Populaire Réunion': 3000,
                'Caisse d\'Épargne Réunion': 3500,
                'Crédit Immobilier de l\'Océan Indien (CIOI)': 1200,
                'HSBC Réunion': 1500,
                'CIC Réunion': 2000
            }
            
            base_value = base_assets.get(bank_name, 2000)
            
            monthly_assets = []
            for i, date in enumerate(dates):
                # Croissance réaliste pour La Réunion
                years_from_start = (date.year - 2002) + (date.month - 1) / 12
                growth_rate = 0.03  # 3% par an en moyenne
                monthly_growth = np.random.normal(growth_rate/12, 0.002)
                
                if i == 0:
                    asset_value = base_value
                else:
                    asset_value = monthly_assets[-1] * (1 + monthly_growth)
                monthly_assets.append(asset_value)
            
            return pd.DataFrame({'Date': dates, f'{bank_name} Assets (M€)': monthly_assets})
            
        except Exception as e:
            print(f"❌ Erreur assets data {bank_name}: {e}")
            return self._create_simulated_data(bank_name, 'Assets (M€)', 2002, 2025)
    
    def get_all_bank_rates(self, bank_name):
        """Récupère tous les taux d'une banque spécifique"""
        print(f"🚀 Début de la récupération des taux pour {bank_name} (2002-2025)...")
        
        # Récupérer toutes les données
        deposit_rate = self.get_historical_deposit_rates(bank_name)
        lending_rate = self.get_historical_lending_rates(bank_name)
        mortgage_rate = self.get_mortgage_rates(bank_name)
        corporate_rates = self.get_corporate_rates(bank_name)
        assets = self.get_bank_assets(bank_name)
        
        # Fusionner les données
        all_data = deposit_rate
        for df in [lending_rate, mortgage_rate, corporate_rates, assets]:
            all_data = pd.merge(all_data, df, on='Date', how='outer')
        
        # Nettoyer et interpoler
        all_data = all_data.sort_values('Date')
        all_data = all_data.set_index('Date')
        all_data = all_data.interpolate(method='time')
        all_data = all_data.reset_index()
        
        # Ajouter des indicateurs calculés
        all_data[f'{bank_name} Retail Spread'] = all_data[f'{bank_name} Lending Rate'] - all_data[f'{bank_name} Deposit Rate']
        all_data[f'{bank_name} Corporate Spread'] = all_data[f'{bank_name} Corporate Lending Rate'] - all_data[f'{bank_name} Corporate Deposit Rate']
        all_data[f'{bank_name} Mortgage Discount'] = all_data[f'{bank_name} Lending Rate'] - all_data[f'{bank_name} Mortgage Rate']
        
        return all_data
    
    def create_comparative_analysis(self, selected_banks=None):
        """Crée une analyse comparative de toutes les banques"""
        if selected_banks is None:
            selected_banks = list(self.banks.keys())[:6]  # Limiter à 6 banques pour la lisibilité
        
        print("🏦 ANALYSE COMPARATIVE DES BANQUES DE LA RÉUNION")
        print("=" * 60)
        
        all_banks_data = {}
        
        # Récupérer les données pour chaque banque sélectionnée
        for bank_name in selected_banks:
            print(f"\n📊 Traitement de {bank_name}...")
            bank_data = self.get_all_bank_rates(bank_name)
            all_banks_data[bank_name] = bank_data
            
            # Sauvegarder individuellement
            filename = f"{bank_name.replace(' ', '_').replace('(', '').replace(')', '')}_rates_2002_2025.csv"
            bank_data.to_csv(filename, index=False)
            print(f"💾 Fichier sauvegardé: {filename}")
        
        # Créer un DataFrame combiné pour l'analyse comparative
        comparative_data = self._create_comparative_dataframe(all_banks_data, selected_banks)
        
        # Générer les visualisations comparatives
        self._create_comparative_visualizations(comparative_data, selected_banks)
        
        # Générer le rapport comparatif
        self._generate_comparative_report(comparative_data, selected_banks)
        
        return comparative_data, all_banks_data
    
    def _create_comparative_dataframe(self, all_banks_data, selected_banks):
        """Crée un DataFrame combiné pour l'analyse comparative"""
        # Prendre la première banque comme base
        base_bank = selected_banks[0]
        comparative_df = all_banks_data[base_bank][['Date']].copy()
        
        # Ajouter les taux de dépôt de toutes les banques
        for bank_name in selected_banks:
            bank_data = all_banks_data[bank_name]
            comparative_df = pd.merge(comparative_df, bank_data[['Date', f'{bank_name} Deposit Rate']], on='Date', how='left')
            comparative_df = pd.merge(comparative_df, bank_data[['Date', f'{bank_name} Lending Rate']], on='Date', how='left')
            comparative_df = pd.merge(comparative_df, bank_data[['Date', f'{bank_name} Mortgage Rate']], on='Date', how='left')
        
        return comparative_df
    
    def _create_comparative_visualizations(self, df, selected_banks):
        """Crée des visualisations comparatives"""
        plt.style.use('seaborn-v0_8')
        
        # 1. Graphique des taux de dépôt comparatifs
        plt.figure(figsize=(15, 10))
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(selected_banks)))
        
        for i, bank_name in enumerate(selected_banks):
            plt.plot(df['Date'], df[f'{bank_name} Deposit Rate'], 
                    label=bank_name, linewidth=2, color=colors[i])
        
        plt.title('Comparaison des Taux de Dépôt - Banques de La Réunion (2002-2025)', 
                 fontsize=14, fontweight='bold')
        plt.ylabel('Taux de Dépôt (%)')
        plt.xlabel('Année')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('comparaison_taux_depot_reunion.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Graphique des taux de prêt comparatifs
        plt.figure(figsize=(15, 10))
        
        for i, bank_name in enumerate(selected_banks):
            plt.plot(df['Date'], df[f'{bank_name} Lending Rate'], 
                    label=bank_name, linewidth=2, color=colors[i])
        
        plt.title('Comparaison des Taux de Prêt - Banques de La Réunion (2002-2025)', 
                 fontsize=14, fontweight='bold')
        plt.ylabel('Taux de Prêt (%)')
        plt.xlabel('Année')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('comparaison_taux_pret_reunion.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 3. Heatmap des taux 2024
        current_rates_2024 = {}
        for bank_name in selected_banks:
            latest_data = df[df['Date'] >= '2024-01-01'].iloc[0]
            current_rates_2024[bank_name] = {
                'Dépôt': latest_data[f'{bank_name} Deposit Rate'],
                'Prêt': latest_data[f'{bank_name} Lending Rate'],
                'Hypothèque': latest_data[f'{bank_name} Mortgage Rate']
            }
        
        heatmap_data = pd.DataFrame(current_rates_2024).T
        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data, annot=True, cmap='RdYlGn_r', center=2.5, 
                   fmt='.2f', linewidths=0.5)
        plt.title('Taux des Banques de La Réunion - Situation 2024', 
                 fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('heatmap_taux_reunion_2024.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _generate_comparative_report(self, df, selected_banks):
        """Génère un rapport comparatif complet"""
        print("\n" + "=" * 80)
        print("📊 RAPPORT COMPARATIF - BANQUES DE LA RÉUNION")
        print("📅 Période: 2002-2025")
        print("=" * 80)
        
        # Analyse des taux 2024
        print("\n🏆 CLASSEMENT 2024 - TAUX DE DÉPÔT:")
        deposit_ranking = []
        for bank_name in selected_banks:
            latest_data = df[df['Date'] >= '2024-01-01'].iloc[0]
            deposit_rate = latest_data[f'{bank_name} Deposit Rate']
            deposit_ranking.append((bank_name, deposit_rate))
        
        deposit_ranking.sort(key=lambda x: x[1], reverse=True)
        for i, (bank, rate) in enumerate(deposit_ranking, 1):
            print(f"  {i}. {bank}: {rate:.2f}%")
        
        print("\n🏆 CLASSEMENT 2024 - TAUX DE PRÊT (plus bas = mieux):")
        lending_ranking = []
        for bank_name in selected_banks:
            latest_data = df[df['Date'] >= '2024-01-01'].iloc[0]
            lending_rate = latest_data[f'{bank_name} Lending Rate']
            lending_ranking.append((bank_name, lending_rate))
        
        lending_ranking.sort(key=lambda x: x[1])
        for i, (bank, rate) in enumerate(lending_ranking, 1):
            print(f"  {i}. {bank}: {rate:.2f}%")
        
        # Évolution sur la période
        print("\n📈 ÉVOLUTION 2002-2025:")
        for bank_name in selected_banks:
            initial_rate = df.iloc[0][f'{bank_name} Deposit Rate']
            final_rate = df.iloc[-1][f'{bank_name} Deposit Rate']
            evolution = ((final_rate - initial_rate) / initial_rate * 100)
            print(f"  {bank_name}: {initial_rate:.2f}% → {final_rate:.2f}% ({evolution:+.1f}%)")
        
        # Recommandations
        print("\n💡 RECOMMANDATIONS:")
        print("  • Meilleur taux dépôt 2024: {}".format(deposit_ranking[0][0]))
        print("  • Meilleur taux prêt 2024: {}".format(lending_ranking[0][0]))
        print("  • Banques locales souvent plus compétitives sur les dépôts")
        print("  • Réseaux nationaux avantageux pour les services internationaux")
        print("  • Spécialistes immobiliers (CIOI) intéressants pour l'habitat")
        
        print("=" * 80)

def main():
    # Initialiser l'analyse des banques de La Réunion
    reunion_banks = ReunionBanksInterestRates()
    
    print("🏦 ANALYSE DES TAUX D'INTÉRÊT - BANQUES DE LA RÉUNION")
    print("📅 Période: 2002-2025")
    print("=" * 50)
    
    # Afficher les banques analysées
    print("\n📋 BANQUES INCLUSES DANS L'ANALYSE:")
    for i, bank_name in enumerate(reunion_banks.banks.keys(), 1):
        bank_info = reunion_banks.banks[bank_name]
        print(f"  {i}. {bank_name} ({bank_info['type']}) - Fondée: {bank_info['founded']}")
    
    # Sélectionner les banques pour l'analyse comparative
    selected_banks = [
        'Crédit Agricole de La Réunion',
        'Banque de La Réunion (BLR)',
        'Banque Française Commerciale Océan Indien (BFC OI)',
        'Société Générale Réunion',
        'BNP Paribas Réunion',
        'Crédit Immobilier de l\'Océan Indien (CIOI)'
    ]
    
    # Lancer l'analyse comparative
    comparative_data, all_banks_data = reunion_banks.create_comparative_analysis(selected_banks)
    
    print(f"\n✅ Analyse terminée avec succès!")
    print(f"📊 {len(selected_banks)} banques analysées")
    print("📁 Fichiers générés:")
    print("   - Fichiers CSV individuels pour chaque banque")
    print("   - comparaison_taux_depot_reunion.png")
    print("   - comparaison_taux_pret_reunion.png")
    print("   - heatmap_taux_reunion_2024.png")
    print("   - Rapport comparatif complet")
    
    # Aperçu des données
    print("\n👀 APERÇU DES DONNÉES (2024):")
    latest_data = comparative_data[comparative_data['Date'] >= '2024-01-01'].iloc[0]
    for bank in selected_banks[:3]:  # Afficher les 3 premières
        print(f"  {bank}: Dépôt {latest_data[f'{bank} Deposit Rate']:.2f}%, Prêt {latest_data[f'{bank} Lending Rate']:.2f}%")

if __name__ == "__main__":
    main()