(function($) {
    $(document).ready(function() {
        var $murdersField = $('#id_murders');
        var $suspectsField = $('#id_suspects');
        var $investigatorsField = $('#id_investigators');
        
        function updateDropdowns() {
            var murderId = $murdersField.val();
            
            if (murderId) {
                // Clear existing options
                $suspectsField.empty().append('<option value="">---------</option>');
                $investigatorsField.empty().append('<option value="">---------</option>');
                
                // Get suspects for this murder
                $.ajax({
                    url: '/ajax/get-suspects/',  // Changed from '/main/ajax/get-suspects/'
                    data: {
                        'murder_id': murderId
                    },
                    success: function(data) {
                        $.each(data.suspects, function(i, suspect) {
                            $suspectsField.append($('<option></option>').attr('value', suspect.id).text(suspect.name));
                        });
                    },
                    error: function(xhr, status, error) {
                        console.log('Error loading suspects:', error);
                    }
                });
                
                // Get investigators for this murder
                $.ajax({
                    url: '/ajax/get-investigators/',  // Changed from '/main/ajax/get-investigators/'
                    data: {
                        'murder_id': murderId
                    },
                    success: function(data) {
                        $.each(data.investigators, function(i, investigator) {
                            $investigatorsField.append($('<option></option>').attr('value', investigator.id).text(investigator.name));
                        });
                    },
                    error: function(xhr, status, error) {
                        console.log('Error loading investigators:', error);
                    }
                });
            } else {
                // Clear dropdowns if no murder selected
                $suspectsField.empty().append('<option value="">---------</option>');
                $investigatorsField.empty().append('<option value="">---------</option>');
            }
        }
        
        // Trigger update when murder selection changes
        $murdersField.change(updateDropdowns);
        
        // Initialize on page load
        updateDropdowns();
    });
})(django.jQuery || jQuery || $);