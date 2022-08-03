# <img src="https://github.com/xie1027/EquityLens/blob/main/logo.png?raw=true" alt="drawing" width="70"/> Equity Lens | DEI Toolbox  


EquityLens is an open-source library that aims to improve the data quality during pre-processing through equity lens.

1. It assesses whether and why disparities exist. Currently, we enable pinpointing disparity in model outcomes; however, we don’t explain why these disparities exist and what contributes to them.  

2. Most tools mitigate unfairness and disparity in the labels, which achieve equal outcomes. Equality produces fair products when society is structured in a fair way. However, when society lacks justice, equality no longer distributes the same resources to all populations. That’s where Equity plays a role.  

Check out [EquityLens](https://github.com/Citi-Ventures/EquityLens)


## Installation and updating
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install or uninstall EquityLens like below. 

```bash
pip install git+ssh://git@github.com/Citi-Ventures/EquityLens.git
pip uninstall EquityLens
```

We use SSH keys authentication to install this package, as this is stored under a private Github repo. You can find the instruction [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

```bash
# 1. Generating a new SSH key
# Paste the text below, substituting in your GitHub email address.
$ ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. Adding your SSH key to the ssh-agent
# Start the ssh-agent in the background.
$ eval "$(ssh-agent -s)"

# 3. Modify your ~/.ssh/config file to automatically load keys into the ssh-agent and store passphrases in your keychain
$ touch ~/.ssh/config
$ open ~/.ssh/config
# add the following to the file    
    Host *
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile ~/.ssh/id_ed25519

# 4. Add your SSH private key to the ssh-agent and store your passphrase in the keychain
$ ssh-add -K ~/.ssh/id_ed25519

# 5. Adding the new SSH key to your GitHub account
# Copy the SSH public key to your clipboard
pbcopy < ~/.ssh/id_ed25519.pub
```

## Usage
Features:
* functions.company_dei_score  --> evaluate a company's DEI efforts in three dimensions
* functions.sample_dei_score  --> evaluate data samples' representation, and generate proxies for protected-class indicators
* functions.compute_score  --> calculate DEI scores based on a specific definition of Diversity and Inclusion ('variety', 'separation', 'disparity')
* functions.root_cause  --> calculate the top 10% of the features with statistically significant difference in mean
* functions.counterfactual_transformation  -->  replace the values among the unprivileged group with their closest neighbor in the privileged group
* functions.Equity_Lens  --> correct important features 


#### Demo of some of the features:
```python
import EquityLens

token = 'replace-with-your-token'
EquityLens.functions.company_dei_score("Citigroup", token)

company_list = ['FLWS', 'ATNF', 'RETC', 'ONCP', 'RTNB', 'C']
EquityLens.functions.sample_dei_score(company_list, token)


var_list = [0.11853823, 0.061011526, 0.114244634, 2.617285942]
EquityLens.functions.compute_score(var_list, 'variety' , 'Finance', token)

protected_class = 'sex'
feature = 'salary'
features = ['salary', 'work experience']
df = some_dataframe
favor = 1

EquityLens.functions.ttest_var(protected_class, feature, some_dataframe)
EquityLens.functions.Equity_Lens(protected_class, features, some_dataframe)
EquityLens.functions.counterfactual_transformation(feature, favor, 'premuium', df)
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
