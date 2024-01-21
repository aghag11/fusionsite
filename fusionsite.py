import streamlit as st
import numpy as np
import plotly.graph_objs as go

# Define the fusion function
def fusion(n, T, E, tau):
    reactivity = n * T
    reaction_rate = reactivity * E
    energy_loss = n * T / tau
    net_energy_output = reaction_rate - energy_loss
    return net_energy_output

# Function to perform grid search within user-defined ranges
def find_best_parameters(n_range, T_range, E_range, tau_range):
    max_output = -np.inf
    best_params = {}
    for n in n_range:
        for T in T_range:
            for E in E_range:
                for tau in tau_range:
                    output = fusion(n, T, E, tau)
                    if output > max_output:
                        max_output = output
                        best_params = {'n': n, 'T': T, 'E': E, 'tau': tau}
    return best_params, max_output

# Function to create plots for parameter impact analysis
def create_parameter_impact_plots(selected_parameter, n, T, E, tau):
    param_range = np.linspace(0.1, 2, 100)
    outputs = []

    if selected_parameter == 'Particle Density':
        for val in param_range:
            outputs.append(fusion(val * n, T, E, tau))
        x_label = 'Particle Density Multiplier'
    elif selected_parameter == 'Temperature':
        for val in param_range:
            outputs.append(fusion(n, val * T, E, tau))
        x_label = 'Temperature Multiplier'
    elif selected_parameter == 'Energy Release':
        for val in param_range:
            outputs.append(fusion(n, T, val * E, tau))
        x_label = 'Energy Release Multiplier'
    else:  # Confinement Time
        for val in param_range:
            outputs.append(fusion(n, T, E, val * tau))
        x_label = 'Confinement Time Multiplier'

    fig = go.Figure(data=go.Scatter(x=param_range, y=outputs))
    fig.update_layout(title=f'Energy Output vs. {selected_parameter}',
                      xaxis_title=x_label,
                      yaxis_title='Energy Output')
    return fig

# Main function where the Streamlit app is defined
def main():
    st.sidebar.title("Fusion Simulator")
    page = st.sidebar.selectbox("Select a page:", 
                                ["Welcome", "Simulation", "Optimization", "Parameter Impact Analysis", "Additional Resources"])

    if page == "Welcome":
        st.title("👋 Welcome to Fusion Simulator ☀️")
        st.write("Explore the fascinating world of nuclear fusion. Adjust parameters, simulate reactions, and discover the future of clean energy!")
        
        if st.button("Get Started"):
            st.sidebar.selectbox("Select a page:", 
                                 ["Welcome", "Simulation", "Optimization", "Parameter Impact Analysis", "Additional Resources"], 
                                 index=1)

        with st.expander("Learn More"):
            st.write("""
                Nuclear fusion is the process of combining two light atomic nuclei to form a heavier nucleus, releasing a significant amount of energy. This process, which powers stars, has the potential to be a source of nearly limitless clean energy if controlled fusion can be achieved on Earth.
            """)

    elif page == "Simulation":
        st.title("Fusion Reaction Simulation")
        n_value = st.slider("Particle Density (n) x10^20", min_value=0.1, max_value=10.0, value=1.0)
        T_value = st.slider("Temperature (T) in keV", min_value=1000.0, max_value=50000.0, value=15000.0)
        E_value = st.slider("Energy Release per Reaction (E) in MeV", min_value=0.1, value=17.6)
        tau_value = st.slider("Energy Confinement Time (τ) in seconds", min_value=0.01, value=0.1)
        energy_output = fusion(n_value * 1e20, T_value, E_value, tau_value)
        st.metric(label="Energy Output", value=f"{energy_output:.2e}")

    elif page == "Optimization":
        st.title("Optimization")
        n_min, n_max = st.slider("Particle Density (n) range x10^20", 1.0, 10.0, (1.0, 5.0))
        T_min, T_max = st.slider("Temperature (T) range in keV", 5000.0, 20000.0, (5000.0, 15000.0))
        E_min, E_max = st.slider("Energy Release (E) range in MeV", 15.0, 25.0, (15.0, 20.0))
        tau_min, tau_max = st.slider("Confinement Time (τ) range in seconds", 0.01, 1.0, (0.05, 0.2))

        if st.button('Find Best Parameters'):
            n_range = np.linspace(n_min * 1e20, n_max * 1e20, 10)
            T_range = np.linspace(T_min, T_max, 10)
            E_range = np.linspace(E_min, E_max, 10)
            tau_range = np.linspace(tau_min, tau_max, 10)
            best_params, max_output = find_best_parameters(n_range, T_range, E_range, tau_range)
            st.write(f"Maximum Energy Output: {max_output:.2e}")
            st.json(best_params)

    elif page == "Parameter Impact Analysis":
        st.title("Parameter Impact Analysis")
        selected_parameter = st.selectbox("Select a parameter to analyze its impact:",
                                          ["Particle Density", "Temperature", "Energy Release", "Confinement Time"])
        n_value = 1e20  # Default value for particle density
        T_value = 15000  # Default value for temperature
        E_value = 17.6  # Default value for energy release
        tau_value = 0.1  # Default value for confinement time

        fig = create_parameter_impact_plots(selected_parameter, n_value, T_value, E_value, tau_value)
        st.plotly_chart(fig)

    elif page == "Additional Resources":
        st.title("Additional Resources")
        st.markdown("""
            Hey! Thank you so much for using my Fusion Simulator :) I've been working on this for the past couple of months with the main goal of helping others really understand what's going on in fusion, because trust me, it's some pretty complicated stuff 😅. I hope you enjoyed, check out some of these additional projects I've created in the space, and feel free to always reach out to me here -> [LinkedIn](https://www.linkedin.com/in/amrita-ghag/)

            Ps: Add any feedback + suggestions YOU have for Fusion Simulator here -> [Feedback Form](https://99p4fpcnzi4.typeform.com/to/bqEQjls2)

            Further reading and resources:
            - [Plasma Instabilities in Fusion Reactors](https://medium.com/@amritaghag08/plasma-instabilities-in-fusion-reactors-a-surrogate-model-approach-to-fusion-reactor-optimization-d0f88afa246e)
            - [Triple Product: Decoding the Most Important Metric in Fusion Reactors](https://medium.com/@amritaghag08/triple-product-decoding-the-most-important-metric-in-fusion-reactors-b89a49c84565)
            - [Enhancing Fusion Reactors Through the Lawson Criterion](https://medium.com/@amritaghag08/enhancing-fusion-reactors-through-the-lawson-criterion-b868e973d357)
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()



