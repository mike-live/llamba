TRANSLATIONS: dict[str, str] = {
    "increased": "an increased",
    "reduced": "a reduced",
    "feature_analysis_prompt": "What is {feature}? What does {level} level of {feature} mean?",
    "disease_risk_prompt_1": "Given the following parameters, estimate the risk of {disease_short_name} (ICD: {disease_icd}) occurring: ",
    "disease_risk_prompt_2": "{param}: {value}, acceleration: {acc}\n",
    "basic_answer_1": "Your bioage is {bio_age} and your aging acceleration is {acceleration}, which means ",
    "ageing_quicker": "you are ageing quicker than normal.\n\n",
    "ageing_slower": "you are ageing slower than normal.\n\n",
    "ageing_normally": "you are ageing normally.\n\n",
    "more_info": "\n\nHere is some more information about your data. \n\n",
    "inflammatory_risk": "How likely you are to get the following inflammatory diseases. \n\n",
    "context": "Use the following information as context: {context}",
    "clock": "Use {clock_name} (DOI: {clock_doi}) for a reference as an immunological clock. ",
    "mortality_opening": "Assessment of diagnosis and risk of adverse outcome in patients with {name}: ",
    "mortality_0": "the risk of adverse outcome is low or non-existent.\n\n",
    "mortality_1": "the risk of adverse outcome is present. \n\n",
    "recommendations_1": "Given the analysis results that will follow, what would you recommend to normalize the results and lower the chance of disease occurrence?",
    "recommendations_2": "Take into account that the person has worked in {condition_name} for {condition_duration}.",
    "recommendations_3": "Explain each recommendation in detail. \n The analysis:\n {analysis}",
    "additional_analysis": "\n\nAdditional analysis\n\n",
    "format_prompt": "You are given a data report. Structure it in the following way: " \
        "1) Show bioage and age acceleration." \
        "2) List the most influential parameters and their values as a table with the Feature, Value, Age acceleration columns." \
        "3) Give a short description for each most influential parameter and what it means if the value is greater/smaller than normal." \
        "4) Provide information about the risk of disease occurrence as a table with the Disease, Risk, Comments columns." \
        "5) Describe in detail how each disease is associated with parameters." \
        "6) Add any auxiliary data that from the Additional analysis part of the report."
        "Make sure that the structured report is in English." \
        "The report is as follows: {analysis}"
}