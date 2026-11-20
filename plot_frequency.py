import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns


def main():
    # File paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    traci_csv = os.path.join(base_dir, 'traci_frequency.csv')
    grpc_csv = os.path.join(base_dir, 'grpc_frequency.csv')
    libsumo_csv = os.path.join(base_dir, 'libsumo_frequency.csv')
    output_png = os.path.join(base_dir, 'frequency_vs_runtime.png')

    # Load data
    print("Loading benchmark CSV files...")
    df_traci = pd.read_csv(traci_csv)
    df_grpc = pd.read_csv(grpc_csv)
    df_libsumo = pd.read_csv(libsumo_csv)

    # Standardize column headers
    for df in [df_traci, df_grpc, df_libsumo]:
        df.columns = df.columns.str.strip().str.upper()

    # Style matching the sample plot
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1.5)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    # 1. Legacy TraCI (Solid Dark Orange)
    sns.lineplot(
        data=df_traci,
        x='FREQUENCY',
        y='TIME',
        color='darkorange',
        linestyle='-',
        linewidth=2.5,
        label='Legacy TraCI',
        ax=ax,
        errorbar='sd'
    )

    # 2. gRPC (Dashed Medium Blue)
    sns.lineplot(
        data=df_grpc,
        x='FREQUENCY',
        y='TIME',
        color='mediumblue',
        linestyle='--',
        linewidth=2.5,
        label='gRPC',
        ax=ax,
        errorbar='sd'
    )

    # 3. Libsumo (Dash-Dot Forest Green)
    sns.lineplot(
        data=df_libsumo,
        x='FREQUENCY',
        y='TIME',
        color='forestgreen',
        linestyle='-.',
        linewidth=2.5,
        label='Libsumo',
        ax=ax,
        errorbar='sd'
    )

    # Keep frequencies (0.1, 1, 10, 100) evenly spaced along the x-axis
    ax.set_xscale('log')
    ax.set_xticks([0.1, 1, 10, 100])
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:g}'))
    ax.xaxis.set_minor_locator(ticker.NullLocator())

    # Configure labels and title
    ax.set_xlabel('Synchronization Frequency (Hz)', fontweight='bold', labelpad=10)
    ax.set_ylabel('Wall-Clock Execution Time (Seconds)', fontweight='bold', labelpad=10)
    ax.set_title('Simulation Runtime: TraCI vs. gRPC vs. Libsumo', fontweight='bold', pad=15)

    # Legend matching sample plot
    ax.legend(
        title='Protocol / Architecture\n(*Shaded area = ±1 Standard Deviation)',
        title_fontsize='12',
        fontsize='12',
        loc='upper left',
        frameon=True,
        framealpha=0.9,
        edgecolor='gray'
    )

    plt.tight_layout()
    plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[OK] Plot successfully generated and saved to: {output_png}")


if __name__ == '__main__':
    main()
